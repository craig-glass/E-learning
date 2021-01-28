# Project Name

ROHAN BHALLA
Description goes here

## Installation

STUART LEWIS
To begin with enter a command line and move to the directory you wish to clone
this repository into using the command: `cd your/directory/path` where
'your/directory/path' is the path name to the desired directory.
 
Next type in the following:

```
git clone https://github.com/craig-glass/E-learning.git
```

### Local Setup (development)


Windows:

Once you have cloned the project onto your local machine, you will need to install the requirements. 
In the command line, type:

pipenv update

This should install all of the dependencies from the requirements.txt file.

This project has been configured to work with a postgresql database so you will need to install postgresql
if you haven't already got it installed. You can download postgresql on windows, mac and linux using the following
link:

https://www.postgresql.org/download/

You will need to add the postgresql bin directory path to the PATH environment variable. It will
look something like this:

C:\Program Files\PostgreSQL\12\bin

This step enables you to use the command psql to start the PostgreSQL command-line tool (psql) from the Windows Command Prompt.
Enter into postgres command line with the following command:

psql -U <username>
  
If you don't set your own username then the default username should be postgres. You may aslo need to specify localhost, like this:

psql -h localhost -U <username>

Create a database with the command:

CREATE DATABASE <database-name>
  
Now you can navigate into your database with:

\c <database-name>
  
To connect to your database you will need to configure it in your config.settings.py file.


This is done in
the config.settings.py file. Add the following to the settings.py file:

DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': '<name-of-database>',
      'USER': '<your-postgres-username>',
      'PASSWORD': '<postgres-password>',
      'HOST': 'localhost',
      'PORT': '5432'
}

Now the database is setup you will need to run migrations to populate the database with the models from the project:
Make sure you are out of the psql command prompt and back in your project root directory and type:

python manage.py makemigrations

And then:

python manage.py migrate

The project should now be ready to run locally at localhost:<port>. 
Run the project with the following command:
  
  python manage.py runserver
  
This will run the project on port 8000, the default port, but if you wish to specify which port 
you would like it to run on, then simply add the number of the port to the end of the command:

  python manage.py runserver 700

Here I have chosen port 700 but any port that is not already in use will work.

That's it, you should have now successfully deployed the app on your local machine.

### Remote Setup


You will need a heroku account for this step. You can sign up here:

https://signup.heroku.com/ 

Once you have a heroku account, install the heroku command prompt:

https://devcenter.heroku.com/articles/heroku-cli

Now you can create an app with:

heroku create <app-name>

In your heroku account you will see your app. In your app, navigate to the resources tab and chose find more add-ons. 
Find heroku postgres and add the add-on to your app. You should now see heroku postgres in your list of installed add-ons on your app dashboard. Click on it, then click on settings, then 'view credentials'.
Here you will find the necessary information to set your variables in the config.setting.py file.

Most of the configuration is already setup to deploy in a production environment to heroku so only a few things will need changing in the config.settings.py file. 

First, change the DEBUG variable to False. We don't want any sensitive data shown to users. 
Second, change the variables in DATABASES to match your postgresql database on heroku.

Now that your database is configured for your heroku postgres database, you can go ahead and make migrations. This will create all of the necessary tables in your database using the django models from the app:

python manage.py makemigrations

python manage.py migrate

Your database for your heroku account will now be created and ready to use.

You have created a heroku app but you are yet to push your local repository. Do this now:

git add .

git commit -m "<your commit message>"
 
git push heroku master

You will be given a link with your apps domain name at the end of the build log in your terminal. Keep a note of this.
Now that you have successfully pushed your app to heroku, all you need to do is scale your dynos for deployment with the following command:

heroku ps:scale web=1

The number here is the number of dynos you would like running for that particular process. 1 dyno will get the app up and running but the performance will not be that great, especially if you are expecting a lot of traffic. Increasing the number here will allow heroku to rout HTTP requests across more running instances of your web servers which will increase performance. 

You can also scale vertically, adding dynos for worker processes which will allow your app to deal with a larger volumer of jobs:

heroku ps: scale worker=1

Or in one command:

heroku ps: scale web=1 worker=1

That's it. Your app should now be up and running. You can view it by clicking 'Open App' in heroku, or just type the name of your site into the website.

## Usage

### Student view

Registered Courses:

Students can view module content, watch lectures, submit assignments, and take
quizzes. It is also possible for students to keep track of their progress
through the analytics section in the user profile area. The announcements page
will hold notifications set by a member of staff for a given course for
students to view.

### Staff view

Staff can create/modify announcements, content, lectures, assignments, and
quizzes. Members of staff also have permissions to view and edit student
details, either through the user's settings page or through the admin, as well
as being able to view any students analytics.

### Admin view

Admins (superusers) can modify contents of the database directly through the
admin view under the url (/admin). Staff also have limited access to this view.

## Support

Craig Glass - b8036820@newcastle.ac.uk

Rohan Bhalla - b9027570@newcastle.ac.uk

Stuart Lewis - b9050231@newcastle.ac.uk

Tiger Kato - b9035378@newcastle.ac.uk

## Authors and acknowledgment

Craig Glass - Team Leader, Courses app, Students app

Rohan Bhalla - PWA, Calendar app, Announcements app

Stuart Lewis - Accounts app, CSS & design, Announcements app

Tiger Kato - Testing

## License

[MIT](https://choosealicense.com/licenses/mit/)
