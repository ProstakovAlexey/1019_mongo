pypy3_gunicorn -D -b 0.0.0.0:8080 -t90 --log-file log1.txt -p bot1.pid -w1 app:api
pypy3_gunicorn -D -b 0.0.0.0:8081 -t90 --log-file log2.txt -p bot2.pid -w1 app:api
pypy3_gunicorn -D -b 0.0.0.0:8082 -t90 --log-file log3.txt -p bot3.pid -w1 app:api
pypy3_gunicorn -D -b 0.0.0.0:8083 -t90 --log-file log4.txt -p bot4.pid -w1 app:api
#gunicorn -D -b 0.0.0.0:8443 -t90 --log-file log.txt -p bot.pid -w1 --certfile=sert/bot.pem --keyfile=sert/bot.key app:api

