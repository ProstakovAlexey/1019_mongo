import time
import random
from multiprocessing.dummy import Pool as ThreadPool
import http.client
import sys
import csv
import smev

"""
Изменение скорости отправки запросов
"""
dir_name = 'for_test'
# Куда отправлять
TI = dict()
TI['snd_name'] = 'СОЦИНФОРМТЕХ'
TI['snd_code'] = 'SOCP01711'
TI['oktmo'] = '70000000'
TI['url'] = '/1019'
TI['adr'] = '192.168.0.195'
TI['port'] = '80'
TI['servicecode'] = '123456789'

# Выполнил подготовку
with open('shablons/Request_1019.xml', mode='r', encoding='utf-8') as fp:
    shablon = fp.read()
# Подменить стандарные поля СМЭВ
shablon = smev.change(shablon, TI)


def send_req(peoples):
    # Создать запрос на основе шаблона и словаря с параметрами
    con = http.client.HTTPConnection(TI['adr'], TI['port'])
    # Соединяется с веб-сервисом, игнорировать проблему с сертификатом
    #con = http.client.HTTPSConnection(TI['adr'], TI['port'], context=ssl._create_unverified_context())
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    for people in peoples:
        request = shablon.format(**people)
        result = None
        try:
            con.request("POST", TI['url'], request.encode('utf-8'), headers=headers)
            result = con.getresponse().read()
            result = result.decode('utf-8')
            #print(result)
        except:
            Type, Value, Trace = sys.exc_info()
            print("Не удалось обратится к методу http://socit.ru/socpayment_tumen, возникли ошибки:")
            print("Тип:", Type, "Значение:", Value)
            print("Выполнение будет продолжено")
            result = None
    con.close()
    return result


if __name__ == '__main__':
    print('Готовлюсь тестировать 1019 сервис')
    # Заполняю список тестовых людей
    tests = list()
    with open('peoples/people_0.txt', encoding='utf-8') as cf:
        data = csv.reader(cf, delimiter=';')
        for row in data:
            people = dict()
            people['FamilyName'] = row[0]
            people['FirstName'] = row[1]
            people['Patronymic'] = row[2]
            people['BirthDate'] = row[3]
            people['Snils'] = '11122233344'
            tests.append(people)
    # Сколько примеров генерить
    n = 8000
    print('Подготовил для отправки %s примеров' % len(tests))
    if len(tests) < n:
        print('мало примеров')
        exit(1)
    # Делаем отправку в несколько потоков
    for thread in (1, 3, 5): #, 7, 10, 12, 15, 20 , 25):
        start = time.time()
        # Заполняем списки с ФИО для каждого потоков
        for_test = list()
        i = 0
        while i<thread:
            one_test = list()
            j = 0
            while j<n:
                one_test.append(random.choice(tests))
                j += 1
            i += 1
            for_test.append(one_test)
        stop = time.time()
        print('Генерация примеров для %s потоков заняла %s сек' % (thread, stop - start))
        print('Начинаю отправку в %s потоков' % thread)
        start = time.time()
        pool = ThreadPool(thread)
        # Это многопоточная отправка
        pool.map(send_req, for_test)
        pool.close()
        pool.join()
        stop = time.time()
        print('Отправляли %s запросов в %s потоков' % (n, thread))
        print('потрачено времени %s сек' % (stop-start))
        print('общая скорость отправки - %s запросов в секунду' % (n/(stop-start)))
        print('скорость в одном потоке - %s запросов в секунду' % (n/(stop-start)/thread))
    exit(0)
