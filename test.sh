#!/bin/sh

###### SWITCHES

# Switch list
# Expected : [{"id": <first id>}, ...]
curl -i -X GET http://localhost:5000/switches/

# Switch 1 status
# Expected :
# {
#    "id": 1,
#    "name": <switch name>,
#    "status": <switch status>,
#    "code": <switch code>,
#    "number": <switch number>,
#    "command": "srcswitch"
# }
curl -i -X GET http://localhost:5000/switches/0/

# Activate switch 1
# Expected : { "id": 1, "status": 1}
curl -i -X GET http://localhost:5000/switches/0/1/

# De-activate switch 1
# Expected : { "id": 1, "status": 0}
curl -i -X GET http://localhost:5000/switches/0/0/

###### SENSORS

# Sensors list
# Expected : [{"id": <first id>}, ...]
curl -i -X GET http://localhost:5000/sensors/

# Sensor 0 value
# Expected :
# {
#    "id": 0,
#    "name": <sensor name>,
#    "value": <sensor value (>0)>,
#    "cache": <cache value>,
#    "command": <command>
# }
curl -i -X GET http://localhost:5000/sensors/0/

# Invalid Sensor value
# Expeced : {}
curl -i -X GET http://localhost:5000/sensors/0/

