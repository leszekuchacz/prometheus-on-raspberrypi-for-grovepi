from grove_rgb_lcd import *
import json,os,time,grovepi,requests, logging
from filelock import Timeout, FileLock

# grovepi envs
grovepi_lock_file_path=str("/code/var/"+os.environ.get('grovepi_lock_file_name','grovepi.lock'))
grovepi_lock_additional_wait_end_seconds=float(os.environ.get('grovepi_lock_additional_wait_end_seconds','1'))
grovepi_button_dport=int(os.environ.get('grovepi_button_dport','3'))

# Logs
log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOGLEVEL', 'ERROR').upper())
stream = logging.StreamHandler()
stream.setLevel(os.environ.get('LOGLEVEL', 'ERROR').upper())
stream.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
log.addHandler(stream)


if __name__ == '__main__':
  lock = FileLock(grovepi_lock_file_path,timeout=10)
  log.info("Starting grovepi_input")
  time.sleep(30) #startup delay
  while True:
    time.sleep(1)
    if grovepi_button_dport>=0:
      with lock:
        lock.acquire()
        log.debug("Lock acquire")
        if grovepi.digitalRead(grovepi_button_dport):
          log.info("Button pressed")
          # TODO: action ex: sth to print on lcd
        time.sleep(grovepi_lock_additional_wait_end_seconds) # time for bus
        log.debug("Lock relase")
        lock.release()
