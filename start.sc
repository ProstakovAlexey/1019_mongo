gunicorn -D -b 0.0.0.0:8443 -t90 --log-file log.txt -p bot.pid -w1 --certfile=sert/bot.pem --keyfile=sert/bot.key app:api

