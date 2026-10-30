[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=24255260)
# CS1520 Project 2

## Goal:
To gain experience using Flask and building data models via an ORM by
developing a website to help manage a catering company.

## High-level description:
You will be writing a website to help manage a catering company. To accomplish
this, you will need to consider three classes of users: the owner of the
company, company staff, and registered customers. Customers will request events
on given days (or cancel events they had previously requested), staff will sign
up to work events, and the owner will be given a rundown of what events are
scheduled and who is working each event. The company cannot schedule more than
1 event per day, and each event needs only 3 Staff members to run.

## Specifications:
1. You must build your website using Python, Flask, SQLAlchemy, and the
	Flask-SQLAlchemy extension.

1. Managing users
	* Each user (Owner, Staff, or Customer) should have a username and
		password.
	* Customers are free to register for their own account.
	* Staff accounts must be created by the Owner (it is fine for the Owner
		to set passwords for the Staff).
	* If a user is logged in, no matter what page they are on, they should
		have access to a logout link.

1. Owner
	* Should be able to login with the username `owner` and password `pass`.
	* Once logged in, the Owner should be presented with a link to create new
		staff accounts, and a list of all scheduled events.
		* For each event, the Staff members signed up to work that event should
			be listed.
		* If no events are scheduled, a message should be displayed informing
			the Owner of this explicitly.
		* If any scheduled event has no staff signed up to work, a message
			should be displayed informing the Owner of this explicitly.

1. Staff
	* Once logged in, Staff members should be presented with a list of events
		they are scheduled to work and a list of events that they can sign up to
		work.
		* For each event that a Staff member can sign up to work, they should
			be provided a link to sign up for that event.
		* No event that already has 3 Staff members signed up to work should be
			presented as a sign up option for other Staff members.

1. Customers
	* Once logged in, Customers should be presented with a form to request a
		new event, and a list of events they have already requested.
		* If a Customer requests an event on a date when another event is
			already scheduled, they should be presented with an message saying
			that the company is already booked for that date.
		* For each requested event, the Customer should be provided with a link
			to cancel that event.

1. Data management
	* To ease bootstrapping and testing of your application, you can hardcode the
		Owner's username and password in your app to be `owner` and `pass`.
	* All other data for your application should be stored in an SQLite
		database named `catering.db` using SQLAlchemy's ORM and the
		Flask-SQLAlchemy extension.

1. Setup
	* You must setup and run Flask within a virtual environment. A
		`requirements.txt` file has been added to the repository for you to use
		in setting up your virtual environment. This is the same
		`requirements.txt` your TA will use to test your project. *Do not* add
		your virtual environment folder to your repository. I suggest you
		name your virtual environment folder `venv`, as you repo is setup
		to ignore this folder by default (see `.gitignore` for details).

## Submission Guidelines:
* **DO NOT SUBMIT** any IDE package files.

* Do not include `catering.db` in your submitted repository.

* You must name the main flask file for your site `catering.py`, and place it
	in the root directory of your repository.

* You must be able to initialize your database with `flask --app catering.py initdb`

* You must be able to run your application with `flask --app catering.py run`

* You must fill out `INFO_SHEET.txt`.

* Be sure to remember to push the latest copy of your code back to your GitHub
	repository before submitting. To submit, log into GradeScope from Canvas and
	have GradeScope pull your repository from GitHub.

## Additional Notes/Hints:
* You may find it handy to use the HTML `date` input type for event
	scheduling.

* While you are not going to be heavily graded on the style and design of your
	web site, it should be presented in a clear and readable manner.

* Your project submissions will be tested using a recent version of Google
	Chrome.

## Grading Rubric:
| Feature | Points
| ------- | ------:
| Owner login set correctly | 5%
| Customer registration | 5%
| Staff account creation | 5%
| Login works appropriately | 15%
| Logout always available and works | 5%
| Owner page displays as specified | 15%
| Staff page displays as specified | 5%
| Staff work sign up works | 10%
| Customer page displays as specified | 5%
| Customer create event works | 10%
| Customer cancel event works | 10%
| Clear and readable presentation | 5%
| Submission/info sheet | 5%
