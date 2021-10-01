curl -XPOST -H "Content-Type: application/json"  localhost:8082/webhook -d "$(cat <<EOF
{
  "receiver": "grovepi_reciver",
  "status": "warning",
  "alerts": [{
    "status": "warning",
    "labels": {
      "alertname": "grovepi_dht_sensor",
      "instance": "grovepi_receiver",
      "severity": "warning"
    },
    "annotations": {
      "summary": "Temp is over 25 C",
      "description": "Open windows"
    },
    "startsAt": "2019-03-14T17:05:37.903Z",
    "endsAt": "0001-01-01T00:00:00Z"
  }],
  "groupLabels": {
    "alertname": "something_happened"
  },
  "commonLabels": {
    "severity": "warning"
  },
  "version": "3",
  "groupKey": 666
}
EOF
)"
