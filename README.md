# Lab-Manager

The new Lab management software to implement pay-per-use concept for the Fab Lab Siegen

## Disclaimer

This project is prototype and still in development. There is no setup script or so. The code is just a snapshot to show how the concept could work.

## Project Status

![Lab Manager](https://github.com/FabLabSiegen/Lab-Manager/workflows/Lab%20Manager/badge.svg?branch=master)

## Key features

- Monitor and Assign available printer to visiting customers in the lab
- Access control via ESP8266 and RFID-reader by connecting/disconnecting OctoPrint to printer
- Store and retrieve print usage details
- Calculate, view and manage cost of each print
- Manage Maintenance of each printer by tracking print hours

## Project Links

- [Architecture](https://drive.google.com/file/d/16qB0iT30ZRu07Zg9T2nqXLLCi88Ac29D/view?usp=sharing)
- [High level user tasks](https://drive.google.com/file/d/1WH51V1CVpxdZxaitDeyuj2zDtwwMi52o/view?usp=sharing)
- [How to use the application](https://drive.google.com/file/d/1tR145jTIe74obSpfrPw2ca4HzGGN9U2-/view?usp=sharing)

# Setup

## ESP_RFID

Implementation for the ESP8266 that controls the RFID-Reader, interprets OctoPrint events and publishes MQTT commands to the broker

Path : ESP_RFID/ESP_RFID.ino

- Open the file ESP_RFID.ino in Arduino IDE (or) any preferred IDE
- Add required libraries ([ArduinoJson](https://arduinojson.org/?utm_source=meta&utm_medium=library.properties), [MFRC522](https://github.com/miguelbalboa/rfid), [PubSubClient](https://github.com/knolleary/pubsubclient)) to the IDE
- Search for the string "# WARNING", then Add Wi-Fi credentials and MQTT connection details
- Search for "# WARNING add RFID tag" and add RFID tag corresponding to the printer
- [Setup NodeMCU with RFID](https://content.instructables.com/ORIG/FX4/GP96/J48Q18RQ/FX4GP96J48Q18RQ.png)
- Upload the code

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
  3. Dependencies such as [django-rest-framework](https://www.django-rest-framework.org/) a powerful and flexible toolkit for building Web APIs, [psycopg2](https://pypi.org/project/psycopg2/) (PostgreSQL database adapter for Python), [django-cors-headers](https://pypi.org/project/django-cors-headers/) (for allowing resources to be accessed on other domains), [simplejson](https://pypi.org/project/simplejson/) as json encoder/decoder are used to build the API.
     Install the dependencies needed to run the app:
     ```bash
         $ pip install -r requirements.txt
     ```
  4. [Setup local Postgres-DB](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

     - Add credentials and db name in `settings.py`

  5. [paho-mqtt](https://pypi.org/project/paho-mqtt/) as MQTT client is used to connect to an MQTT broker to publish messages, and to subscribe to topics and receive published messages. In the file lab_manager\mqttservice.py, search for "WARNING add MQTT Host" and add MQTT host details

  6. Make those migrations work
     ```bash
         $ python manage.py makemigrations
         $ python manage.py migrate
     ```

- #### Run It
  Fire up the server using this one simple command:
  ```bash
      $ python manage.py runserver 8080
  ```
  You can now access the api endpoints on your browser.
- #### End points of REST API:

  - `GET, POST` printers detail available in Lab: ` api/printers`
  - `GET, PUT` each printer detail available in Lab: ` api/printers/{string:id}`
  - `GET, POST` user detail available in Lab: ` api/user`
  - `GET, PUT` each user detail available in Lab: ` api/user/{string:user}`
  - `GET, POST, DELETE` usage detail available in Lab: ` api/usage`
  - `GET, PUT, DELETE` each usage detail available in Lab: ` api/usage/{string:id}`
  - `GET` filament detail available in Lab: ` api/filament`
  - `GET, PUT` each filament detail available in Lab: ` api/filament/{string:filamentname}`
  - `GET, PUT` default material usage details: ` /api/material/{string:id}`
  - `GET, PUT` default printer usage details: ` /api/printer/{string:id}`
  - `GET, PUT` default operating usage details: ` /api/operating/{string:id}`

## Front-End (React App)

![Application view](https://github.com/FabLabSiegen/Lab-Manager/blob/newfeature/Uploads/Application_preview.gif)

Path : Lab-manager/Front-End

To get the Front-End application running locally:

- Install Node JS. Refer to https://nodejs.org/en/ to install nodejs.

- Install create-react-app npm package globally. This will help to easily run the project and also build the source files easily. Use the following command to install create-react-app

```bash
         $ npm install -g create-react-app
```

- Navigate to folder Lab-Manager/Front-End from command line

```
         $ cd Lab-Manager/Front-End
```

- Install all required dependencies. The Front-end is built using packages [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/) as css framework, [React-Hooks](https://reactjs.org/docs/hooks-intro.html) for state management, [Axios](https://www.npmjs.com/package/axios) as HTTP client,

```
         $ npm install
```

- Start the local server (this project uses [create-react-app](https://reactjs.org/docs/create-a-new-react-app.html))

```
         $ npm start
```

Local web server will use port 8081 instead of standard React's port 3000 to prevent conflicts with some backends like Node. Port can be onfigured in scripts section of `package.json`. Once the Django API is running, Front-end starts interacting with the API.

## OctoPrint Setup for testing

OctoPrint is used to control and monitor every aspect of your 3D printer and your printing jobs right from within your browser.

- Setup OctoPrint based on your device, refer to https://octoprint.org/download/

- For installing OctoPrint on your local windows machine, refer to https://community.octoprint.org/t/setting-up-octoprint-on-windows/383.

- Once the OctoPrint is installed, create account and connect to Virtual Printer ([The Virtual Printer plugin](https://docs.octoprint.org/en/master/development/virtual_printer.html#enabling-the-virtual-printer) provides a virtual printer to connect to during development. The virtual printer has been included in OctoPrint by default. This plugin allows you to debug OctoPrint’s serial communication without connecting to an actual printer. Furthermore, it is possible to create certain edge conditions that may be hard to reproduce with a real printer).

- Add [MQTT plugin](https://plugins.octoprint.org/plugins/mqtt/) and [MQTT Subscribe](https://plugins.octoprint.org/plugins/mqttsubscribe/) plugins to the OctoPrint to Pubilish/Subscribe messages from MQTT Broker. Refer procedure for adding plugins in OctoPrint https://plugins.octoprint.org/help/installation/

- Configure [MQTT plugin](https://plugins.octoprint.org/plugins/mqtt/) by entering MQTT connection details under Broker tab and configure topics using base topic: OctoPrint as [shown](https://github.com/FabLabSiegen/Lab-Manager/blob/newfeature/Uploads/MQTT_plugin_setup1.PNG)

- Configure [MQTT Subscribe](https://plugins.octoprint.org/plugins/mqttsubscribe/) plugin as [shown](https://github.com/FabLabSiegen/Lab-Manager/blob/newfeature/Uploads/MQTT_Subscribe_setup.png).
