from grove_rgb_lcd import *
import json,os,time,grovepi,requests
from filelock import Timeout, FileLock

# grovepi envs
grovepi_lock_file_path=str("/code/var/"+os.environ.get('grovepi_lock_file_name','grovepi.lock'))
grovepi_button_dport=int(os.environ.get('grovepi_button_dport','3'))

if __name__ == '__main__':
  lock = FileLock(grovepi_lock_file_path,timeout=10)
  while True:
    time.sleep(1)
    if grovepi_button_dport>=0:
      with lock:
        lock.acquire()
        if grovepi.digitalRead(grovepi_button_dport):
          print("button pressed")
          # TODO: action ex: sth to print on lcd
        lock.release()
