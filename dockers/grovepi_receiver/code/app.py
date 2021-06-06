from grove_rgb_lcd import *
from wsgiref.simple_server import make_server
import falcon,json,os,time,grovepi

grovepi_rgb_lcd=os.environ.get('grovepi_rgb_lcd','false')
grovepi_buzzer_dport=int(os.environ.get('grovepi_buzzer_dport','-1'))
grovepi_led_red_dport=int(os.environ.get('grovepi_led_red_dport','-1'))
# buzzer
def notify_buzzer(t: float):
  try:  
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
    grovepi.pinMode(grovepi_led_red_dport,"OUTPUT")
    grovepi.digitalWrite(grovepi_led_red_dport,1)
    time.sleep(1)
    grovepi.digitalWrite(grovepi_led_red_dport,0)
  except Exception as e:
    print(e)

# Rgb_lcd
def rgb_lcd_clear():
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
    data = req.get_media()
    print("group_status: "+data['status'])
    for a in data['alerts']:
      print("  alert_status: "+a['status']+" alertname: "+a['labels']['alertname']+" severity: "+a['labels']['severity']+" desc: "+a['annotations']['description'])

      output=a['labels']['severity']+": "+a['labels']['alertname']
      if grovepi_buzzer_dport >= 0:
        notify_buzzer(0.1)  
      if grovepi_led_red_dport >= 0:
        notify_led(a['labels']['severity'])
      if grovepi_rgb_lcd == "true":
        notify_lcd_rgb(output,a['labels']['severity'])
    resp.status = falcon.HTTP_200

app = falcon.App()
app.req_options.auto_parse_form_urlencoded=True
app.add_route('/webhook',WebhookResource())

if __name__ == '__main__':
  if grovepi_rgb_lcd == "true":
    notify_lcd_rgb("Starting...","resolved")
  with make_server('', 8082, app) as httpd:
    httpd.serve_forever()
