import threading
from .mqttservice import mqttserviceThread
default_app_config = 'lab_manager.apps.LabManagerConfig'


stop_thread = threading.Event()
service_thread = mqttserviceThread(stop_thread)
service_thread.start()
