gunicorn -D -b unix:/tmp/gunicorn1.sock -t90 --log-file log.txt -p bot.pid -w7 app:api
#gunicorn -D -b 0.0.0.0:8080 -t90 --log-file log.txt -p bot.pid -w4 app:api
#gunicorn -D -b 0.0.0.0:8443 -t90 --log-file log.txt -p bot.pid -w1 --certfile=sert/bot.pem --keyfile=sert/bot.key app:api

