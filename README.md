prometheus-on-raspberrypi-for-grovepi
=======================================
A stack of monitoring solutions for Raspberrypi orchestrated by `docker-compose` based on [Prometheus](https://github.com/prometheus/prometheus), [Grafana](https://github.com/grafana/grafana) and [AlertManager](https://github.com/prometheus/alertmanager).

# Stack overview
+ **groviepi_reciever** - http endpoint for alertmanager, gives avaiablity to push alerts from alertmanager to lcd or buzzier. 
+ **groviepi_exporter** - http endpoint for prometheus, gives availability to scrape groviepi sensor metrics. 
+ **node_exporter**     - http endpoint for prometheus, gives availability to scrape host metrcis(cpu,mem).
+ **prometheus**        - monitoring tool, database for grafana. 
+ **grafana**           - visualizations of scraped metrics. 
+ **alertmanager**      - push alerts from promethesus to defined targets(groviepi_reciever).


# Install(fast and default)
1. You  need to install raspbian 10 for architecture **arm64** on  your raspberry pi. [raspbian 10 arm64](https://downloads.raspberrypi.org/raspios_arm64/images/). You can base on this instruction [www.raspberrypi.org](https://www.raspberrypi.org/documentation/installation/installing-images/)

2. Login on root, run bellow command and reboot.
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
3. After reboot we're ready to run this stack.
```
git clone git@github.com:leszekuchacz/prometheus-on-raspberrypi-for-grovepi.git
cd prometheus-on-raspberrypi-for-grovepi
docker-compose build
docker-composer up -d
```
4. After get status 'done' for all containers, you can try check default endpoint:


|  Address              | container_name  |
|-----------------------|---------------  |
| http://localhost:8081 | grovepi_exporter|
| http://localhost:9100 | node_exporter   |
| http://localhost:8082 | grovepi_receiver|
| http://localhost:9093 | alertmanager    |
| http://localhost:9090 | prometheus      |
| http://localhost:3000 | grafana         |

