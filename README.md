# Lab-Manager

The new Lab management software to implement pay-per-use concept for the Fab Lab Siegen

## Disclaimer

This project is not ready to use and still in development. There is no setup script or so. The code is just a snapshot to show how it could work.
Search for the string "# WARNING". You need to add your credentials for MQTT broker, WIFI and database where you find this string with an applicable note.

## Project Status

![Lab Manager](https://github.com/FabLabSiegen/Lab-Manager/workflows/Lab%20Manager/badge.svg?branch=master)

## Key features

- Switch plugwise plugs on and off via RFID chips
- Access control via ESP8266 and RFID-reader
- Device management of plugwise devices, RFID chips and ESP8266 via webinterface
- Usermanagement via webinterface
- Communication between ESPs and backend via MQTT

## Project Links

- [Architecture](https://drive.google.com/file/d/16qB0iT30ZRu07Zg9T2nqXLLCi88Ac29D/view?usp=sharing)
- [User tasks](https://drive.google.com/file/d/1WH51V1CVpxdZxaitDeyuj2zDtwwMi52o/view?usp=sharing)
- [Interaction Flow](https://drive.google.com/file/d/1tR145jTIe74obSpfrPw2ca4HzGGN9U2-/view?usp=sharing)

## Setup

<hr />

## ESP_RFID

Implementation for the ESP8266 that controls the RFID-Reader, interprets OctoPrint events and publishes MQTT commands to the broker

Path : ESP_RFID/ESP_RFID.ino

- Open the file ESP_RFID.ino in Arduino IDE (or) any preferred IDE
- Add required libraries ([ArduinoJson](https://arduinojson.org/?utm_source=meta&utm_medium=library.properties), [MFRC522](https://github.com/miguelbalboa/rfid), [PubSubClient](https://github.com/knolleary/pubsubclient)) to the IDE
- Search for the string "# WARNING", then Add Wi-Fi credentials and MQTT connection details
- Search for "# WARNING add RFID tag" and add RFID tag corresponding to the printer
- [Setup NodeMCU with RFID](https://content.instructables.com/ORIG/FX4/GP96/J48Q18RQ/FX4GP96J48Q18RQ.png)
- Upload the code

<hr />

## Lab-Manager (Django rest framework + Postgres-DB)

Back-End of the application is a REST api built using Django rest framework with Postgres-DB.

## Installation

- If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
- After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
  ```bash
      $ pip install virtualenv
  ```
- Then, Git clone this repo to your PC

  ```bash
      $ git clone https://github.com/FabLabSiegen/Lab-Manager.git
  ```

- #### Dependencies

  1. Cd into your the cloned repo as such:
     ```
         $ cd Lab-Manager
     ```
  2. Create and fire up your virtual environment:
     ```bash
         $ virtualenv  venv -p python3
         $ source venv/bin/activate
     ```
  3. Install the dependencies needed to run the app:
     ```bash
         $ pip install -r requirements.txt
     ```
  4. [Setup local Postgres-DB](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

     - Add credentials and db name in `settings.py`

  5. Make those migrations work
     ```bash
         $ python manage.py makemigrations
         $ python manage.py migrate
     ```

- #### Run It
  Fire up the server using this one simple command:
  ```bash
      $ python manage.py runserver 8080
  ```
  You can now access the api service on your browser.
- #### End points of REST API:

  - GET, POST printers detail available in Lab: ` api/printers`
  - GET, PUT each printer detail available in Lab: ` api/printers/{string:id}`
  - GET, POST user detail available in Lab: ` api/user`
  - GET, PUT each user detail available in Lab: ` api/user/{string:user}`
  - GET, POST, DELETE usage detail available in Lab: ` api/usage`
  - GET, PUT, DELETE each usage detail available in Lab: ` api/usage/{string:id}`
  - GET filament detail available in Lab: ` api/filament`
  - GET, PUT each filament detail available in Lab: ` api/filament/{string:filamentname}`
  - GET, PUT default material usage details: ` /api/material/{string:id}`
  - GET, PUT default printer usage details: ` /api/printer/{string:id}`
  - GET, PUT default operating usage details: ` /api/operating/{string:id}`
  <hr />

## Front-End (React App)

<hr />

## OctoPrint Setup
