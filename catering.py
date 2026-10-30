from functools import wraps 
from datetime import datetime 
import os 

from flask import(
    Flask,render_template,request,redirect,
    url_for,session,flash
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config["SECRET_KEY"]= "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"]=(
    "sqlite:///" + os.path.join(app.root_path, "catering.db")
)
db= SQLAlchemy(app)

event_staff=db.Table(
    "event_staff",
    db.Column(
        "event_id",
        db.Integer, 
        db.ForeignKey("event.id"),
        primary_key=True
    ),
    db.Column(
        "staff_id", 
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True
    )

)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    role= db.Column(db.String(20), nullable=False)

    customer_events=db.relationship(
        "Event",
        backref="customer",
        lazy=True
    )

    staff_events=db.relationship(
        "Event",
        secondary=event_staff,
        back_populates="staff"
    )
   

class Event(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date,unique=True,nullable=False)
    description=db.Column(db.String(300),nullable=False)

    customer_id=db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    staff= db.relationship(
        "User",
        secondary=event_staff,
        back_populates="staff_events"
    )

def current_user():
    user_id= session.get("user_id")

    if user_id is None:
        return None
    return db.session.get(User,user_id)

def login_required(view):
    @wraps(view)
    def wrapped(*args,**kwargs):
        if session.get("role")=="owner" or current_user():
            return view(*args,**kwargs)
        flash("Please log in first.")
        return redirect(url_for("login"))
    return wrapped 
def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            if(session.get("role")=="owner"):
                role="owner"
            else:
                user=current_user()
                role=user.role if user else None 
            if role not in roles: 
                flash("You do not have permission to acess that page.")
                return redirect(url_for("dashboard"))
            return view(*args,**kwargs)
        return wrapped
    return decorator  

@app.context_processor
def inject_user():
    return{
        "logged_in_user": current_user(),
        "current_role": session.get("role")
    }

@app.cli.command("initdb")
def initdb():
    """Create all database tables."""
    db.create_all()
    print("Database initialized sucessfully!")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username","").strip()
        password=request.form.get("password", "")

        if(username=="owner" and password=="pass"):
            session.clear()
            session["role"]= "owner"
            flash("Welcome,Owner!")
            return redirect(url_for("dashboard"))
        
        user=User.query.filter_by(username=username).first()

        if(user and check_password_hash(user.password,password)):
            session.clear()
            session["user_id"]= user.id
            session["role"]= user.role 

            flash("Login successful!")
            return redirect(url_for("dashboard"))
        flash("Incorrect username or password.")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username", "").strip()
        password=request.form.get("password","")

        if not username or not password:
            flash("Please enter a username and password.")
            return redirect(url_for("register"))
        
        existing_user=User.query.filter_by(username=username).first()
        if existing_user:
            flash("That username is already taken.")
            return redirect(url_for("register"))

        new_user=User(
            username=username,
            password=generate_password_hash(password),
            role="customer"
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! You can now log in.")
        return redirect(url_for("login"))
        
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    role= session.get("role")

    if(role=="owner"):
        return redirect(url_for("owner_dashboard"))
    user=current_user()

    if user.role=="staff":
        return redirect(url_for("staff_dashboard"))
    if user.role=="customer":
        return redirect(url_for("customer_dashboard"))

@app.route("/owner")
@roles_required("owner")
def owner_dashboard():
    events= Event.query.order_by(Event.date).all()

    staff_members= User.query.filter_by(role="staff").order_by(
        User.username
    ).all()

    return render_template(
        "owner.html",
        events=events,
        staff_members=staff_members
    )
@app.route("/owner/create-staff", methods=["GET","POST"])
@roles_required("owner")
def create_staff():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter a username and password.")
            return redirect(url_for("create_staff"))

        if username.lower() == "owner":
            flash("That username is reserved.")
            return redirect(url_for("create_staff"))

        if User.query.filter_by(username=username).first():
            flash("That username is already taken.")
            return redirect(url_for("create_staff"))

        staff_member = User(
            username=username,
            password=generate_password_hash(password),
            role="staff"
        )
        db.session.add(staff_member)
        db.session.commit()

        flash("Staff account created successfully!")
        return redirect(url_for("owner_dashboard"))

    return render_template("create_staff.html")

@app.route("/staff")
@roles_required("staff")
def staff_dashboard():
    user = current_user()
    all_events = Event.query.order_by(Event.date).all()

    assigned_events = [
        event for event in all_events
        if user in event.staff
    ]

    available_events = [
        event for event in all_events
        if user not in event.staff and len(event.staff) < 3
    ]

    return render_template(
        "staff.html",
        assigned_events=assigned_events,
        available_events=available_events
    )
@app.route("/staff/signup/<int:event_id>", methods=["POST"])
@roles_required("staff")
def signup_event(event_id):
    user=current_user()
    event=db.session.get(Event,event_id)

    if event is None:
        flash("That event does not exist.")
    elif user in event.staff:
        flash("You are already signed up for this event.")
    elif len(event.staff)>=3:
        flash("This event already has three staff members.")
    else:
        event.staff.append(user)
        db.session.commit()
        flash("You successfully signed up for the event!")
    return redirect(url_for("staff_dashboard"))
@app.route("/customer")
@roles_required("customer")
def customer_dashboard():
    user= current_user()
    events= Event.query.filter_by(
        customer_id=user.id
    ).order_by(Event.date).all()

    return render_template(
        "customer.html",
        events=events
    )

@app.route("/customer/create-event", methods=["POST"])
@roles_required("customer")
def create_event():
    date_string= request.form.get("date","")
    description= request.form.get("description","").strip()

    if not date_string or not description:
        flash("Please enter an event date and description.")
        return redirect(url_for("cusomter_dashboard"))

        try:
            event_date=datetime.strptime(
                date_string,"%Y-%m-%d".date()
            ).date()
        except ValueError:
            flash("Please enter a valid date.")
            return redirect(url_for("customer_dashboard"))
        if(event_date<datetime.today().date):
            flash("You cannot request an event in the past.")
            return redirect(url_for("customer_dashboard"))

        existing_event=Event.query.filter_by().first()

        if existing_event:
            flash("The company is already booked for that date.")
            return redirect(url_for("customer_dashboard"))
            
        new_event = Event(
            date=event_date,
            description=description,
            customer_id=current_user().id
        )

    db.session.add(new_event)

    try:
        db.session.commit()
        flash("Your event request was submitted successfully!")
    except Exception:
        db.session.rollback()
        flash("That date is already booked.")

    return redirect(url_for("customer_dashboard"))


@app.route("/customer/cancel-event/<int:event_id>", methods=["POST"])
@roles_required("customer")
def cancel_event(event_id):

    user = current_user()

    event = Event.query.filter_by(
        id=event_id,
        customer_id=user.id
    ).first()

    if event is None:
        flash("Event not found.")
        return redirect(url_for("customer_dashboard"))

    db.session.delete(event)
    db.session.commit()

    flash("Your event has been cancelled.")
    return redirect(url_for("customer_dashboard"))
