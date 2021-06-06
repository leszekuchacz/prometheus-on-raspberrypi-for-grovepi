import time, os, grovepi, math, smbus2, bme280
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily, InfoMetricFamily
from prometheus_client import start_http_server, Info

# grovepi envs
grovepi_exporter_port=int(os.environ.get('grovepi_exporter_port','8081'))
grovepi_dht_dport=int(os.environ.get('grovepi_dht_dport','-1'))
grovepi_dht_dport=int(os.environ.get('grovepi_dht_dport','-1'))
grovepi_dht_type=int(os.environ.get('grovepi_dht_type','0'))
grovepi_hcho_aport=int(os.environ.get('grovepi_hcho_aport','-1'))
grovepi_hcho_r0=int(os.environ.get('grovepi_hcho_r0','25'))
grovepi_sound_aport=int(os.environ.get('grovepi_sound_aport','-1'))
grovepi_light_aport=int(os.environ.get('grovepi_light_aport','-1'))
grovepi_barometer_type=str(os.environ.get('grovepi_barometer_type',''))

# alerts envs
alert_temperature_max_warning=int(os.environ.get('alert_temperature_max_warning','26'))
alert_temperature_max_firing=int(os.environ.get('alert_temperature_max_firing','32'))
alert_temperature_min_warning=int(os.environ.get('alert_temperature_min_warning','18'))
alert_temperature_min_firing=int(os.environ.get('alert_temperature_min_firing','5'))
alert_humidity_max_warning=int(os.environ.get('alert_humidity_max_warning','80'))
alert_humidity_max_firing=int(os.environ.get('alert_humidity_max_firing','90'))
alert_humidity_min_warning=int(os.environ.get('alert_humidity_min_warning','20'))
alert_humidity_min_firing=int(os.environ.get('alert_humidity_min_firing','10'))
alert_pressure_max_warning=int(os.environ.get('alert_pressure_max_warning','1020'))
alert_pressure_max_firing=int(os.environ.get('alert_pressure_max_firing','1050'))
alert_pressure_min_warning=int(os.environ.get('alert_pressure_min_warning','980'))
alert_pressure_min_firing=int(os.environ.get('alert_pressure_min_firing','950'))
alert_ppm_max_warning=int(os.environ.get('alert_ppm_max_warning','4'))
alert_ppm_max_firing=int(os.environ.get('alert_ppm_max_firing','10'))
alert_loudless_max_warning=int(os.environ.get('alert_loudless_max_warning','400'))
alert_loudless_max_firing=int(os.environ.get('alert_loudless_max_firing','600'))

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
    if grovepi_barometer_type == "bme280":
      i2c_address=0x76
      bus=smbus2.SMBus(1) # Grove hat rev1 = 1
      calibration_params = bme280.load_calibration_params(bus, i2c_address)
      data = bme280.sample(bus, i2c_address, calibration_params)
      yield GaugeMetricFamily("grovepi_barometer_temperature", '°C', value=data.temperature)
      yield GaugeMetricFamily("grovepi_barometer_humidity", 'rH', value=data.humidity)
      yield GaugeMetricFamily("grovepi_barometer_pressure", 'hPa', value=data.pressure)
    # Info - tresholds for alerts in prometheus
    yield GaugeMetricFamily("alert_temperature_max_warning","",value=alert_temperature_max_warning)    
    yield GaugeMetricFamily("alert_temperature_max_firing", "",value=alert_temperature_max_firing)    
    yield GaugeMetricFamily("alert_temperature_min_warning","",value=alert_temperature_min_warning)    
    yield GaugeMetricFamily("alert_temperature_min_firing", "",value=alert_temperature_min_firing)    
    yield GaugeMetricFamily("alert_humidity_max_warning","",value=alert_humidity_max_warning)    
    yield GaugeMetricFamily("alert_humidity_max_firing", "",value=alert_humidity_max_firing)    
    yield GaugeMetricFamily("alert_humidity_min_warning","",value=alert_humidity_min_warning)    
    yield GaugeMetricFamily("alert_humidity_min_firing", "",value=alert_humidity_min_firing)    
    yield GaugeMetricFamily("alert_pressure_max_warning","",value=alert_pressure_max_warning)    
    yield GaugeMetricFamily("alert_pressure_max_firing", "",value=alert_pressure_max_firing)    
    yield GaugeMetricFamily("alert_pressure_min_warning","",value=alert_pressure_min_warning)    
    yield GaugeMetricFamily("alert_pressure_min_firing", "",value=alert_pressure_min_firing)    
    yield GaugeMetricFamily("alert_ppm_max_warning", "",value=alert_ppm_max_warning)    
    yield GaugeMetricFamily("alert_ppm_max_firing", "",value=alert_ppm_max_firing)    
    yield GaugeMetricFamily("alert_loudless_max_warning", "",value=alert_loudless_max_warning)    
    yield GaugeMetricFamily("alert_loudless_max_firing", "",value=alert_loudless_max_firing)    
    
    
    
    # Can't export label as value, info have always value 1
    #i = InfoMetricFamily("grovie_vars", "T")
    #i.add_metric(labels="sensor", value={ "type": "temperature","name": "max", "severity": "warning", "value": "27"})
    #i.add_metric(labels="sensor", value={"type": "temperature","name": "max", "severity": "firing", "value": "30"})
    #yield i 
      
      
if __name__ == '__main__':
    start_http_server(grovepi_exporter_port)
    REGISTRY.register(CustomCollector())
    while True:
      time.sleep(1)
        
