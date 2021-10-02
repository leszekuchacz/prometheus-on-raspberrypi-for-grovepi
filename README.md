prometheus-on-raspberrypi-for-grovepi
=======================================
A stack of monitoring solutions for Raspberrypi orchestrated by `docker-compose` based on [Prometheus](https://github.com/prometheus/prometheus), [Grafana](https://github.com/grafana/grafana) and [AlertManager](https://github.com/prometheus/alertmanager).

# Stack overview
+ **groviepi_reciever** - http endpoint for alertmanager, gives avaiablity to push alerts from alertmanager to lcd or buzzier. 
+ **groviepi_exporter** - http endpoint for prometheus, gives availability to scrape groviepi sensor metrics. 
+ **groviepi_input**    - Reads the change of button, gives availability to define action under push button( ex. show temp on lcd).
+ **node_exporter**     - http endpoint for prometheus, gives availability to scrape host metrcis(cpu,mem).
+ **prometheus**        - monitoring tool, database for grafana. 
+ **grafana**           - visualizations of scraped metrics. 
+ **alertmanager**      - push alerts from promethesus to defined targets(groviepi_reciever).



# Install(fast and default)
1. You  need to install raspbian 10 for architecture **arm64** on  your raspberry pi. [raspbian 10 arm64](https://downloads.raspberrypi.org/raspios_arm64/images/). You can base on this instruction [www.raspberrypi.org](https://www.raspberrypi.org/documentation/installation/installing-images/)

2. Connect hat and sensors to rasberrypi.


| Name           | SKU       |Link                                                          | Cost| Port to Connect |
|----------------|-----------|--------------------------------------------------------------|-----|-----------------|
| GrovePi+  | 103010002 | https://wiki.seeedstudio.com/GrovePi_Plus/ | $35 | add-on board with 15 Grove 4-pin interfaces that brings Grove sensors |
| dht11 sensor| 101020011 |https://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/ | $6.50 | D7 |
| hcho sensor | 101020001 WSP2110 | https://wiki.seeedstudio.com/Grove-HCHO_Sensor/ | $16.50 | A0 |
| light sensor | 101020132  LS06-S  phototransistor| https://seeeddoc.github.io/Grove-Light_Sensor_v1.2/ | $3.20 | D2|
| lcd rgb backlight| 104030001 6X2 LCD RGB| https://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/| $13.10 | i2c-1 |
| buzzer | 107020000 Piezo Buzzer/Active Buzzer | https://wiki.seeedstudio.com/Grove-Buzzer/ | $2.10 | D8 |
| barometer | 101020193 bme280 | https://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/ | $18.70 |i2c-3 |
| led red | 104030005 | https://wiki.seeedstudio.com/Grove-Red_LED/ | $2.10 | D5 |
| Button | 101020003 | https://seeeddoc.github.io/Grove-Button/ | $2.10 | D3 |

![Host](https://raw.githubusercontent.com/leszekuchacz/prometheus-on-raspberrypi-for-grovepi/develop/docs/connections_v0.3.0.jpg)

3. Login on root, run bellow command and reboot.
```
su
apt-get update && sudo apt-get upgrade
apt-get remove docker docker-engine docker.io containerd runc
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
 echo \
  "deb [arch=arm64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  apt-get install docker-ce docker-ce-cli containerd.io git
  pip3 -v install docker-compose
  usermod -aG docker pi
  reboot
  
```
4. After reboot we're ready to run this stack.
```
git clone git@github.com:leszekuchacz/prometheus-on-raspberrypi-for-grovepi.git
cd prometheus-on-raspberrypi-for-grovepi
docker-compose build
docker-composer up -d
```
5. After get status 'done' for all containers, you can try check default endpoint:


|  Address              | container_name  |
|-----------------------|---------------  |
| http://localhost:8081 | grovepi_exporter|
| http://localhost:9100 | node_exporter   |
| http://localhost:8082 | grovepi_receiver|
| http://localhost:9093 | alertmanager    |
| http://localhost:9090 | prometheus      |
| http://localhost:3000 | grafana         |

![Host](https://raw.githubusercontent.com/leszekuchacz/prometheus-on-raspberrypi-for-grovepi/develop/docs/grafana_v0.3.0.png)
![Host](https://raw.githubusercontent.com/leszekuchacz/prometheus-on-raspberrypi-for-grovepi/develop/docs/prometheus_v0.3.0.png)
