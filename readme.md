# Caller App 
##### *by Prafful Kumar*


#### Python == 3.6.9, Django == 3.0.7
To run the app first create a virtual environment and install the dependencies by running following commands

$ `virtualenv -p /usr/bin/python3.6 caller_app`
$ `pip install -r requirements.txt`

Create a mysql user and database and update the credentials in caller_app/.env , if any

Run the migrations
$ `python manage.py migrate`

Then create a superuser to access the admin panel
$`python manage.py createsuperuser` 

Run the server 
$ `python manage.py runserver`

To run the script to prepoluate the data
$ python manage.py shell
`>>> exec(open('filldb.py').read())`

I have also dumped the data in data.json file which can be used to load initial data
I have also exported the postman collection for the apis.

The project has two apps: -
1) Users - for all users and accounts related stuff
2) Contacts - for all contacts related stuff
Whenever a user is created its contact instance is also created. Spam is handled. Spam count is the count of users which have reported a contact as a spam.
