import time
import os
import grovepi
import math
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server


grovepi_exporter_port=int(os.environ.get('grovepi_exporter_port','8081'))
grovepi_dht_dport=int(os.environ.get('grovepi_dht_dport','-1'))
grovepi_dht_dport=int(os.environ.get('grovepi_dht_dport','-1'))
grovepi_dht_type=int(os.environ.get('grovepi_dht_type','0'))
grovepi_hcho_aport=int(os.environ.get('grovepi_hcho_aport','-1'))
grovepi_hcho_r0=int(os.environ.get('grovepi_hcho_r0','25'))
grovepi_sound_aport=int(os.environ.get('grovepi_sound_aport','-1'))
grovepi_light_aport=int(os.environ.get('grovepi_light_aport','-1'))
grovepi_light_aport=int(os.environ.get('grovepi_light_aport','-1'))

class CustomCollector(object):
  def __init__(self):
    pass

  def collect(self):
    # DHT sensor
    if grovepi_dht_dport >= 0:
      [grovepi_dht_temperature,grovepi_dht_humidity] = grovepi.dht(grovepi_dht_dport,grovepi_dht_type)
      yield GaugeMetricFamily("grovepi_dht_temperature", 'celusish', value=grovepi_dht_temperature)
      yield GaugeMetricFamily("grovepi_dht_humidity", 'hygrometer', value=grovepi_dht_humidity)
      #print("temp = %.02f C humidity =%.02f%%"%(grovepi_dht_temperature, grovepi_dht_humidity))
    # HCHO sensor - Wsp2110
    if grovepi_hcho_aport >= 0:
      sensor_value = grovepi.analogRead(grovepi_hcho_aport)
      # Rs - resistance gas 
      grovepi_hcho_rs = (float)(1024.0 / sensor_value) - 1
      # R0 - Rs on clear air area, for me it is 25
      grovepi_hcho_ppm = math.pow(10.0, ((math.log10(grovepi_hcho_rs/grovepi_hcho_r0) - 0.0827) / (-0.4807)))
      yield GaugeMetricFamily("grovepi_hcho_sensor_value", 'raw', value=sensor_value)
      yield GaugeMetricFamily("grovepi_hcho_rs", 'resistance on gas(Benzene,Toluene,Alcohol)', value=grovepi_hcho_rs)
      yield GaugeMetricFamily("grovepi_hcho_r0", 'resistance on clear air', value=grovepi_hcho_r0)
      yield GaugeMetricFamily("grovepi_hcho_ppm", 'parts per milion', value=grovepi_hcho_ppm)
    # Sound sensor
    if grovepi_sound_aport >= 0:
      yield GaugeMetricFamily("grovepi_sound", 'dB', grovepi.analogRead(grovepi_sound_aport))
    if grovepi_light_aport >= 0:
      yield GaugeMetricFamily("grovepi_light", 'lumen', grovepi.analogRead(grovepi_light_aport))
      
      
if __name__ == '__main__':
    start_http_server(grovepi_exporter_port)
    REGISTRY.register(CustomCollector())
    while True:
      time.sleep(1)
        
