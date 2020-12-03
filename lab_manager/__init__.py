default_app_config = 'lab_manager.apps.LabManagerConfig'


from .fablabcontrol import fablabcontrolThread
import threading

stop_thread = threading.Event()
fab_thread = fablabcontrolThread(stop_thread)
fab_thread.start()