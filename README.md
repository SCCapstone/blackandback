# blackandback

Web-based automatic photo colorizer. Users input a black and white photo and our program colors that photo without any human help.

# Getting Started

## Prerequisites

Running this code locally requires the following software:

    [Python 3.6](https://www.python.org/downloads/)
    [Django 2.1.2 (or other compatable version)](https://www.djangoproject.com/)
    [django-analytical] (due to poorly maintained libraries, installing [pycryptodome] maybe be neccessary for this install)
    [Tensorflow](https://www.tensorflow.org/)
    [Keras](https://keras.io/)
    [Psycopg2]
    [social-auth-app-django]
    [scikit-image]
    [pillow]  
    [progrssbar.js]
    [google_auth_oauthlib]
    [google-api-python-client]
    [oauth2client]
    

Once you have all the prerequisite software installed, go to the *mysite* directory and start the server using

    sudo python3 manage.py runserver 0.0.0.0:80

All that end users need is a photo and an internet connection.

## Note On Operating Systems

A Windows setup is possible, but this software is intended to be run on a Linux machine.

# Our Team

* [Ryan Davis](https://github.com/ryandavis709)
* [Tristan Klintworth](https://github.com/TKlintworth)
* [Allison Rogers](https://github.com/allisonrrogers)
* [Christian Tarque](https://github.com/christiantarque)
* [Connor Taylor](https://github.com/connorrt)

#Testing

Must be using chrome browser and have chromedriver (in path) and selenium installed

Run unit tests by using commands:
cd blackandback/django/django_test/mytestsite
python3 manage.py test

Run behavioral tests with the following commands:
cd blackandback/django/django_test/mytestsite
python3 manage.py runserver

then in a separate terminal window:
cd blackandback/django/django_test/mytestsite/test
./behavior_test.py
