# Lab-Manager
The new Lab management and access control system for the Fab Lab Siegen

## Project Status
![Lab Manager](https://github.com/FabLabSiegen/Lab-Manager/workflows/Lab%20Manager/badge.svg?branch=master)

## Project Plan

* Setup local DB (Status: Done)
* Code Views & Models (Status: Done)
* Testing API end points using [postman](https://www.guru99.com/postman-tutorial.html) (Status: Done)
* Setup unit testing (Status: ToDo)
* Code fabalabcontrol (Status: ToDo)
* Design UI Screens (Status: ToDo)
* Code React App (Status: ToDo)
* Connect React App to REST API (Status: ToDo)
* Complete unit testing (Status: ToDo)



## Setup

### Setup local Postgres-DB
Follow this guide: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04


Credentials and db name are configured in `settings.py`

## Running the REST API

Create the DB tables first:
```
python manage.py migrate
```
Run the development web server:
```
python manage.py runserver 8080
```
##  Endpoints of REST API

* For get, post, delete users: ` /api/login`

* For get, update default material usage details: ` /api/material`

* For get, put default printer usage details: ` /api/printer`

* For get, put default operating details: ` /api/operating`

* For get, post, delete total usage details: ` /api/usage`

* For get, put, delete usage detail of individual record : ` /api/usage/pk`
