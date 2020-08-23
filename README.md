### Sample documents

```json
curl -XPOST 'http://localhost:9200/logs/services' -H 'Content-Type: application/json' -d'
{
	"@timestamp": "2020-08-22T23:56:00",
    "machinename": "node1",
    "servicename": "service1",
    "status": "happy"
}
'
curl -XPOST 'http://localhost:9200/logs/services' -H 'Content-Type: application/json' -d'
{
	"@timestamp": "2020-08-22T23:56:00",
    "machinename": "node1",
    "servicename": "service2",
    "status": "happy"
}
'
curl -XPOST 'http://localhost:9200/logs/services' -H 'Content-Type: application/json' -d'
{
	"@timestamp": "2020-08-22T23:56:00",
    "machinename": "node2",
    "servicename": "service1",
    "status": "happy"
}
'
```
