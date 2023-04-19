from grove_rgb_lcd import *
from wsgiref.simple_server import make_server
import falcon,json,os,logging,time,grovepi,smbus2
from filelock import Timeout, FileLock

# grovepi envs
grovepi_lock_file_path=str("/code/var/"+os.environ.get('grovepi_lock_file_name','grovepi.lock'))
grovepi_lock_additional_wait_end_seconds=float(os.environ.get('grovepi_lock_additional_wait_end_seconds','1'))
grovepi_rgb_lcd=os.environ.get('grovepi_rgb_lcd','false')
grovepi_buzzer_dport=int(os.environ.get('grovepi_buzzer_dport','-1'))
grovepi_led_red_dport=int(os.environ.get('grovepi_led_red_dport','-1'))
grovepi_i2c_motor_driver_address=str(os.environ.get('grovepi_i2c_motor_driver_address',0x03))


log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOGLEVEL', 'ERROR').upper())
stream = logging.StreamHandler()
stream.setLevel(os.environ.get('LOGLEVEL', 'ERROR').upper())
stream.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
log.addHandler(stream)


# I2c motor drive - water the plant(idea)
# PoC (Revisit in Future) - unfortunately this module after connected to any i2c port killing in  1 minute all communication on Grovepi+(rasbian buster 64) :( 
# similar  https://forum.seeedstudio.com/t/grove-i2c-motor-driver-v1-3-is-killing-i2c-communication/257914
class motor_driver:
    MotorSpeedSet             = 0x82
    PWMFrequenceSet           = 0x84
    DirectionSet              = 0xaa
    MotorSetA                 = 0xa1
    MotorSetB                 = 0xa5
    Nothing                   = 0x01
    EnableStepper             = 0x1a
    UnenableStepper           = 0x1b
    Stepernu                  = 0x1c
    I2CMotorDriverAdd         = 0x03  #Set the address of the I2CMotorDriver
    def __init__(self,address=0x03):
        self.I2CMotorDriverAdd=address
    #Maps speed from 0-100 to 0-255
    def map_vals(self,value, leftMin, leftMax, rightMin, rightMax):
        #http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)
        # Convert the 0-1 range into a value in the right range.
        return int(rightMin + (valueScaled * rightSpan))
    #Set motor speed
    def MotorSpeedSetAB(self,MotorSpeedA,MotorSpeedB):
        MotorSpeedA=self.map_vals(MotorSpeedA,0,100,0,255)
        MotorSpeedB=self.map_vals(MotorSpeedB,0,100,0,255)
        bus.write_i2c_block_data(self.I2CMotorDriverAdd, self.MotorSpeedSet, [MotorSpeedA,MotorSpeedB])
        time.sleep(.02)
    #Set motor direction
    def MotorDirectionSet(self,Direction):
        bus.write_i2c_block_data(self.I2CMotorDriverAdd, self.DirectionSet, [Direction,0])
        time.sleep(.02)

# buzzer
def notify_buzzer(t: float):
  try:  
    log.debug("Notify_buzzer")
    grovepi.pinMode(grovepi_buzzer_dport,"OUTPUT")
    grovepi.digitalWrite(grovepi_buzzer_dport,1)
    time.sleep(t)
    grovepi.digitalWrite(grovepi_buzzer_dport,0)
  except Exception as e:
    print(e)
    time.sleep(0.2)
    grovepi.digitalWrite(grovepi_buzzer_dport,0)
    
# led
def notify_led(severity):
  try:  
    log.debug("Notify_led")
    grovepi.pinMode(grovepi_led_red_dport,"OUTPUT")
    grovepi.digitalWrite(grovepi_led_red_dport,1)
    time.sleep(1)
    grovepi.digitalWrite(grovepi_led_red_dport,0)
  except Exception as e:
    print(e)

# Rgb_lcd
def rgb_lcd_clear():
  log.debug("Lcd clear")
  setRGB(0,0,0)
  time.sleep(0.1)
  setText("")

def notify_lcd_rgb(text,severity):
  if severity == "firing":
    setRGB(255,0,0)
  elif severity == "warning":
    setRGB(240,180,0)
  elif severity == "resolved":
    setRGB(0,255,0)
  else:
    setRGB(0,0,255)
  setText(text)
  time.sleep(5)
  rgb_lcd_clear()

# Falcon
class WebhookResource:
  def on_post(self,req,resp):
    lock = FileLock(grovepi_lock_file_path,timeout=10)
    with lock:
      log.debug("Lock acquire")
      lock.acquire()
      data = req.get_media()
      log.info("group_status: "+data['status'])
      for a in data['alerts']:
        #print("  alert_status: "+a['status']+" alertname: "+a['labels']['alertname']+" severity: "+a['labels']['severity']+" desc: "+a['annotations']['description'])
        output=a['labels']['severity']+": "+a['labels']['alertname']
        if grovepi_buzzer_dport >= 0:
          log.debug("Grovepi buzzer dport")
          notify_buzzer(0.1)  
        if grovepi_led_red_dport >= 0:
          log.debug("Grovepi led_red dport")
          notify_led(a['labels']['severity'])
        if grovepi_rgb_lcd == "true":
          log.debug("Grovepi rgb_lcd i2c")
          notify_lcd_rgb(output,a['labels']['severity'])
      log.debug("Lock realease")
      lock.release()      
    resp.status = falcon.HTTP_200

class I2cMotorDriveResource:
  def on_get(self,req,resp):
    resp.text = '{"message": "Only post request support"}'
    resp.status = falcon.HTTP_200

  def on_post(self,req,resp):
    data = json.load(req.bounded_stream)
    print("Power: "+str(data['power'])+", Worktime: "+str(data['worktime'])+", Engine: "+str(data['engine']))
    bus=smbus2.SMBus(1)
    m= motor_driver(bus)
    A=int(0)
    B=int(0)
    if data['engine'] == 'A':
      A=int(data['power'])
    elif data['engine'] == 'B':
      B=int(data['power'])
    else:
      A=int(data['power'])
      B=int(data['power'])
    lock = FileLock(grovepi_lock_file_path,timeout=10)
    with lock:
      lock.acquire()
      m.MotorDirectionSet(0b1010)
      m.MotorSpeedSetAB(A,B)
      time.sleep(int(data['worktime']))
      m.MotorSpeedSetAB(0,0)
      del m
      bus.close()
      time.sleep(grovepi_lock_additional_wait_end_seconds) # time for bus
      lock.release()      
    resp.status = falcon.HTTP_200

app = falcon.App()
app.req_options.auto_parse_form_urlencoded=True
app.add_route('/webhook',WebhookResource())
app.add_route('/motor',I2cMotorDriveResource())

if __name__ == '__main__':
  log.info("Starting grovepi_receiver")
  if grovepi_rgb_lcd == "true":
    lock = FileLock(grovepi_lock_file_path,timeout=10)
    with lock:
      lock.acquire()
      log.debug("Lock acquire")
      notify_lcd_rgb("Starting...","resolved")
    time.sleep(grovepi_lock_additional_wait_end_seconds) # time for bus
    log.debug("Lock release")
    lock.release()      
  with make_server('', 8082, app) as httpd:
    httpd.serve_forever()
