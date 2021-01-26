# E-Learning

Description goes here

## Installation

How to install

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
Find heroku postgres and add the add-on to your app. You should now see heroku postgres in your list of installed add-ons
on your app dashboard. Click on it, then click on settings, then 'view credentials'.
Here you will find the necessary information to set your variables in the config.setting.py file.

Most of the configuration is already setup to deploy in a production environment to heroku so only a few things will
need changing in the config.settings.py file. 

First, change the DEBUG variable to False. We don't want any sensitive data shown to users. 
Second, change the variables in DATABASES to match your postgresql database on heroku.

## Usage

How to use website

## Support

Our contact details

## Contributing

Our stance on contributions

## Authors and acknowledgment

Craig Glass - 
Stuart Lewis - 
Rohan Bhalla - 
Tiger Kato - 

## License

[MIT](https://choosealicense.com/licenses/mit/)
