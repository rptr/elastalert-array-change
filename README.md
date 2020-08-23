### Sample document

curl -XPOST 'http://localhost:9200/logs/services' -H 'Content-Type: application/json' -d'
{
	"@timestamp": "2020-08-22T23:56:00",
    "machinename": "node1",
    "servicename": "service1",
    "status": "happy"
}
'

