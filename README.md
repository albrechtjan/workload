workload
========

Website and API for workload monitoring of students at TU Dresden.

Written by Konstantin Schubert.
Email: konstantin@schubert.fr

This repository containes the code to run the workload monitoring website and the Web-API that is needed by the corresponding workload monitoring Android app. The Android app has its [own repository (and documentation)](https://github.com/KonstantinSchubert/workload-android).

## Technology

Most of the code is written in Python, using the [Django web framework](https://www.djangoproject.com/). The websites themselves are written in HTML and CSS and make use of the Django templating language. If you're new to Django, it is a good idea to try [the very helpful tutorial](https://docs.djangoproject.com/en/1.9/intro/tutorial01/). To store its data, Django uses a [MySQL database](https://www.mysql.com/). Authentication is set up to use the [Shibboleth Single-Sign-On system](https://shibboleth.net/), but it should be easy to switch to another authentication provider or use Djangos built in user management system.

## Architecture

A MySQL database is used to store the data which is entered by the students on the website and which is passed to the API. The database also contains information about the lectures which a student can take. 

There are three main components that connect to the database: The user-facing website, the admin panel, and the API.
This API is used by the [workload Android app](https://github.com/KonstantinSchubert/workload-android) to retrieve and store data. This means that all data is collected in a single place.

All three components use the the Django framework and are defined in a single *Django app*: [workloadApp](https://github.com/KonstantinSchubert/workload/tree/master/server-side/workload/workloadApp).

The project settings are defined in [`workload/settings.py`](https://github.com/KonstantinSchubert/workload/blob/master/server-side/workload/workload/settings.py). You can also check there if you are interested in the configuration of the database that Django uses.

For authentication, the 

## Installation
  * The website is using the [Django web framework](https://www.djangoproject.com/), version 1.9.7 Therefore a web server (apache2, nginx) with an installation of Django and all its dependencies is needed. Django is extremely well documented. For starters, here are:
    * [Installation instructions](https://docs.djangoproject.com/en/1.7/topics/install/)
    * [Deployment instructions](https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/)
    * [A beginners tutorial](https://docs.djangoproject.com/en/1.7/intro/tutorial01/) in case you are intersted in understanding the architecture of django projects and apps.
  * Please consider that Django is under active developmnent and despite the developer's care for backwards compatibility, newer versions of Django might not always work. This project was tested with version 1.9.7, you might have to update the code to run with newer versions. 
  
  * To install the workload project, just clone the repository to your server. The Django project directory is `server-side/workload`.
  * Create an empty file called `workload.log` in the root directory of the repository and make sure that the server-user (usually `www-data`) can write to it. Django will log into this file.
  * [Configure apache for the django project using mod_wsgi.](https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/)
  * If you are using Shibboleth, you will have to set it up for you apache server and make sure all necessary attributes are passed. Your shhibboleth identity provider should be able to assist you with that or point you to the right documentation. You will also have to install the [`django-shibboleth-adapter`](https://github.com/KonstantinSchubert/django-shibboleth-adapter) Django app and configure it to use the right attributes.


## Currently installed setup for `survey.zqa.tu-dresden.de`
 * The current setup is installed on a Debain machine with public DNS `survey.zqa.tu-dresden.de`.
 * The repository which contains the django project is located in `/home/kon`.
 * The django logger writes to `/home/kon/workload/workload.log`
 * Django is installed in a virtual environment which can be activated by entering `workon workload` in the shell.
 * The project is configured to use a MySQL database which is daily backed up into `database-backup`. The file name of the backup which is stored contains the month and day of month. Therefore, once a year, the backup is overwritten. This rotation mechanism should prevent the server from running out of dsik if left unattended for a long time.
 * An apache server is used to serve the site. The necessary configs can be found in `/etc/apache2/sites-enabled/`. Server logs are in `/var/log/apache2`.
 * Shibboleth is used for authentication and installed on the server. The apache `mod_shib` module is activated and the shibboleth configuration can be found in `/etc/shibboleth`.
 * The `django-shibboleth-adapter` is cloned into `/home/kon` and its app directory is symlinked from the Django project directory,  `/home/kon/workload/server-side/workload`


## Download and analyse the data from the database

 * [See here for instructions on how to download the data. ](documentation/ReadoutDatabase.md)
 * [See here for description of the table structure in the database.](documentation/TableStructure.md)
  
  
