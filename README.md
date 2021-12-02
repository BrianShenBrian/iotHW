# iot_hw
How To Run:

$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto

$ cd rest

$ python3 manage.py runserver 0.0.0.0:8000

$cd gRPC

$ python3 fib_server.py

$ python3 log_server.py

How To Use

Post:

$ curl -X POST http://localhost:8000/rest/fib -d '{"order": ORDER_NUMBER}'

GET:

$ curl http://localhost:8000/rest/log
