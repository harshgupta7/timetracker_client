import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import os
import subprocess
from werkzeug import secure_filename

class Watcher:


    DIRECTORY_TO_WATCH = "."

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
                p = subprocess.Popen(['lsappinfo','front'], stdout=subprocess.PIPE)
                result = p.communicate()[0].decode('utf-8')
                p = subprocess.Popen(['lsappinfo', 'info' ,'-only','name','{}'.format(result)], stdout=subprocess.PIPE)
                result = p.communicate()[0].decode('utf-8')
                result = result.split('=', 1)[-1]
                print(result)
                requests.get('https://apptimetracker.herokuapp.com/app/{}'.format(result))
        except:
            self.observer.stop()
            print ("Error")
        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        print(str(event.src_path))
        c = requests.get('https://apptimetracker.herokuapp.com/{}'.format(str(secure_filename(event.src_path))))
        print(c.status_code)

if __name__ == '__main__':
    w = Watcher()
    w.run()