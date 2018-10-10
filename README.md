# Task Manager App
Task logging python tool, structured as a Flask and REST API application

**Task Manager App** is a task logging python tool, structured as a Flask and REST API application.
Jinja2 coding is applied within html to serve data from a Mongo DB database to the front end-user, who can create, edit and delete tasks.

## Features

- Once a user's email is authorised and login credentials are set up, the user can access an online portal where tasks are viewable for all users.
- All users can click and view a task
- However, a task may only be edited by the user who primarily created the task
 
## Task Manager Project Set-Up

- Module pre-requisites are found in the <a href="https://github.com/Kremzeeq/TaskManagerApp/blob/master/requirements.txt"></a> file
- Opening the project in PyCharm should prompt for modules from the file to be installed
- Alternatively use **pip install** for requirements.txt in the command line

## Changes required in Python Code

| Location                           | Guidance                                                                                       |
|:-----------------------------------|:-----------------------------------------------------------------------------------------------|
| src/config.py                      | Substitute ADMINS frozenset email with a preferred email                                       |
| src/run.py                         | Type a port number as per preferences. Port 5000 has been set as the default                   |
| src/models/users/user_constants.py | Substitute variables for URL, AUTH_URL, API_KEY, FROM which can be obtained via Mailgun: https://www.mailgun.com/           |
| src/common.database.py             | Database URI is defaulted to "mongodb://127.0.0.1:27017" for your local machine. Please ammend according to preferences.           |


## MongoDB Database Set-Up

- Mongo DB Community Edition 4.0 was installed for this project
- Manual for installing MongoDB on Linux, macOS and Windows is available here:
https://docs.mongodb.com/manual/administration/install-community/

## Initiating the MongoDB instance

- Once MongoDB has been configured to preferences, ensure **mongod**, the MongoDB daemon, has been typed into the command line.

## Running the application

- Please configure the application to run from the run.py file so that the URI can be accessed

## Accessing the **Task Portal**

- Once the URI is active, the Task Portal may be accessed by clicking "Sign Up" in the top left-hand menu.
- Signing up with your email will trigger an email to be sent with an authorisation code e.g. through using MailGun
- A link within the email will direct you to register with an email and password
- Thereafter the initiation of a Flask user session will redirect you to the Task Portal
- Separately, you can login to access the Task Portal

## Actions within the **Task Portal**

- In the Task Portal you can add new tasks
- Clicking on any listed task enables you to view more details about the task
- If you are the task owner, you will be able to edit or delete the tasks through the UI of the system
- Otherwise edits to the database can be done through using mongoDB in the command line

**Copyright: Sian Thompson (Kremzeeq)**

Author Email: sian.thompson@gmx.co.uk
