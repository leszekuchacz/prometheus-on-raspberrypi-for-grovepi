Testing & helper scripts
===============

1. Testing rgb lcd blackligt and send alert:
```
./alertmanager_push_firing_to_grovepi_receiver.sh
./alertmanager_push_warning_to_grovepi_receiver.sh
./alertmanager_push_resolved_to_grovepi_receiver.sh
```

2. Testing single container, without docker-compose
```
docker run -p 8081:8081 --env-file envs/grovepi --privileged -v /dev/i2c-1:/dev/i2c-1  -v /home/pi/prom/dockers/grovepi_exporter/code:/code -it grovepi_exporter:latest

docker run -v /home/pi/prom/dockers/prometheus/:/etc/prometheus/ -p 9090:9090 -it --env-file /home/pi/prom/envs/grovepi prom/prometheus:v2.27.1 --config.file=/etc/prometheus/prometheus.yml --enable-feature=expand-external-labels

```
