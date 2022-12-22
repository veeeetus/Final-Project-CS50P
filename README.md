# Final-Project-CS50P
## Video Demo: https://youtu.be/wf4V-LxhdOA
# Password Manager
This is my implementation of command-line based password manager written in **Python** <br><br>

## Firstly we have a file called ***project.py*** <br>
It contains **main** function as well as other ones which was a requirement in course specification <br> 
#### Functions
- **Beginning** <br>
    + Imports + starting database engine
- **main** <br>
    + Creates hidden file with an encryption/decryption key which is used with stored on account passwords
    + Starts with anonymous menu which lets you login/register
    + **Case 1 Log in**:
        + if user is logged in new menu appears with options to manage passwords
            + **Case 1 Add Password**:
                * Asks user for site -> login -> password then if everything is valid function sends DML statement to database which saves password with user's id as foreing key
            + **Case 2 List Accounts**:
                * Lists all accounts belonging to logged user
            + **Case 3 List Accounts With Passwords**:
                * Lists all accounts belonging to user with revealed passwords
            + **Case 4 Change Password**:
                * Asks user for id of password which is meant to be changed, then prompts for new password if password is valid DML statement updates password
            + **Case 5 Delete Password**:
                * Asks user for id of password if certain id exists and belongs to logged user DML statement deletes password from database
            + **Case 6 Log out**:
                * Log user out and load anonymous menu
            + **Case 7**:
                * Exits app
    + **Case 2 Register**:
        * Registers user if one passed valid credentials
    + **Case 3 Exit**:
        * Exits app
- **register**:
    + With usage of sqlalchemy and session sends query to database which registers user
- **log_user**:
    + validates password hashes if they match sets **user** variable to user's id which equals to logging user in
- **table**:
    + Prints menu depending on user variable being set to None or id
- **generate_key**:
    + Creates encryption/decryption key in a hidden file in root directory of project
- **get_opt**:
    + Depending on passed to function number (here 3 or 7), will validate if chosen number is in range of valid options from menu and pass or return error message
- **get_username**:
    + Asks user for username then validates it and returns username or error message depending on outcome of validation
- **get_pass**:
    + This function breaks into 3 cases:
        * **Case 1 login**:
            * Validates given password if matches specs returns it elseway shows error message
        * **Case 2 register**:
            * Validates password and compare password to re-typed password if they match returns password
        * **Case 3 site**:
            * Validates password which will be kept on users account
- **get_site**:
    + This one breaks into 2 parts:
        * **Case 1 site**:
            * Asks for name of site/app to which belongs certain password
        * **Case 2 login**:
            * Asks for login to account to certain site/app
<br><br>

## Secondly there is file **classes.py**
Here I store sqlalchemy orm oriented mapping of classes to database tables

<br>

## Last but not least is **test_project.py**
Containts some tests to my project which was one of specifications in course

<br><br>

# Short guide on how to try this project
> Firstly I do not recommend using it generally since I am only learning and this is one of my very first projects, but I will write a simple guide if anyone wants to try it :)
+ **Step 1**:
    * Make a directory and clone git repo from this link *URL*
+ **Step 2**:
    * Create venv and install all packages from **requirements.txt** with pip (e.g. pip install texttable)
+ **Step 3**:
    * Open sqlite and run dumped sql script to create database
    example: app.sql | sqlite3 app.db
+ **Step 4**:
    * type python3 project.py and enjoy your password manager :)
