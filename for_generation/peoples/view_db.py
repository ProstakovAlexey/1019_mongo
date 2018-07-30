from pymongo import MongoClient
import pprint
import function
import time

# Соединение с БД
client = MongoClient('192.168.0.195', 27017)
db = client['1019']
collection = db['payments']

famil = 'Михайлова'
name = 'Зоя'
otch = 'Тестович'
dr = '06.06.1981'
hash = function.hash(famil, name, otch, dr)
start = time.time()
people = collection.find_one({'_id': hash})
print('Время:', time.time()-start)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(people)
client.close()
