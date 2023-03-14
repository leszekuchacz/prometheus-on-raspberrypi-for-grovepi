# Example of adding three kitronikbme688-exporter 
1. Go to place where you clone this repo and run command `docker compose down`
2. Insert below code block to `dockers/prometheus/prometheus.yml`, after the last job in section `scrape_configs`
```
  - job_name: 'kitronikbme688-exporter'
    honor_labels: true
    static_configs:
      - targets: ['192.168.9.101:80']
        labels:
          localization_name: "garage"
  - job_name: 'kitronikbme688-exporter'
    honor_labels: true
    static_configs:
      - targets: ['192.168.9.102:80']
        labels:
          localization_name: "attic"
  - job_name: 'kitronikbme688-exporter'
    honor_labels: true
    static_configs:
      - targets: ['192.168.9.103:80']
        labels:
          localization_name: "outside"

```
3. Start docker compose `docker compose up -d`
