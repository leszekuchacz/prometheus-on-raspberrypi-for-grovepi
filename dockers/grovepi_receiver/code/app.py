from grove_rgb_lcd import *
from wsgiref.simple_server import make_server
import falcon
import json 
import os

grovepi_rgb_lcd=os.environ.get('grovepi_rgb_lcd','false')

# Rgb_lcd
def rgb_lcd_clear():
  setRGB(0,0,0)
  time.sleep(0.1)
  setText("")

def rgb_lcd_notify(text,severity):
    
    if severity == "firing":
      setRGB(255,0,0)
    elif severity == "warning":
      setRGB(255,255,0)
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
      if grovepi_rgb_lcd == "true":
        rgb_lcd_notify(output,a['labels']['severity'])
    resp.status = falcon.HTTP_200

app = falcon.App()
app.req_options.auto_parse_form_urlencoded=True
app.add_route('/webhook',WebhookResource())

if __name__ == '__main__':
  if grovepi_rgb_lcd == "true":
    rgb_lcd_notify("Starting...","resolved")
  with make_server('', 8082, app) as httpd:
    httpd.serve_forever()
