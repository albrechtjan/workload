workload
========

Website and API for workload monitoring of students at TU Dresden.

Written by Konstantin Schubert.
Email: konstantin@schubert.fr

This repository containes the code to run the workload monitoring website and the Web-API that is needed by the corresponding workload monitoring Android app. The Android app has its [own repository (and documentation)](https://github.com/KonstantinSchubert/workload-android).

## Technology

Most of the code is written in Python, using the [Django web framework](https://www.djangoproject.com/). The websites themselves are written in HTML and CSS and make use of the Django templating language. If you're new to Django, it is a good idea to try [the very helpful tutorial](https://docs.djangoproject.com/en/1.9/intro/tutorial01/). To store its data, Django uses a [MySQL database](https://www.mysql.com/).

## Architecture

A MySQL database is used to store the data which is entered by the students on the website and which is passed to the API. The database also contains information about the lectures which a student can take. 

There are three main components that connect to the database: The user-facing website, the admin panel, and the API. 

All three components use the the Django framework and are defined in a single *Django app*: [workloadApp](https://github.com/KonstantinSchubert/workload/tree/master/server-side/workload/workloadApp). The Django app is the only app contained in the Django [workload *project*](https://github.com/KonstantinSchubert/workload/tree/master/server-side/workload). 

The project settings are defined in [workload/settings.py](https://github.com/KonstantinSchubert/workload/blob/master/server-side/workload/workload/settings.py). You can also check there if you are interested in the configuration of the database that Django uses.
