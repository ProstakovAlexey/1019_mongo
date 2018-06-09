import datetime
import time
import random
from multiprocessing.dummy import Pool as ThreadPool
import http.client
import sys
import os
import csv
import smev
import ssl

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
TI['adr'] = 'ti'
TI['port'] = '80'
TI['servicecode'] = '123456789'


def send_req(file_name):
    # Создать запрос на основе шаблона и словаря с параметрами
    # Прочитать шаблон
    with open(file_name, mode='r', encoding='utf-8') as fp:
        request = fp.read()
    # Соединяется с веб-сервисом, игнорировать проблему с сертификатом
    #con = http.client.HTTPSConnection(TI['adr'], TI['port'], context=ssl._create_unverified_context())
    con = http.client.HTTPConnection(TI['adr'], TI['port'])
    # Пытаемся отправить 1-ю часть
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    result = None
    try:

        con.request("POST", TI['url'], request.encode('utf-8'), headers=headers)
        result = con.getresponse().read()
        #result = result.decode('utf-8')
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
    # Выполнил подготовку
    with open('shablons/Request_1019.xml', mode='r', encoding='utf-8') as fp:
        shablon = fp.read()

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
    n = 1000
    file_list = list()
    for i in range(0, n):
        # Подменить стандарные поля СМЭВ
        request = smev.change(shablon, TI)
        # Подменить индивидуальные
        request = smev.change(request, random.choice(tests))
        # Сохранить запрос
        file_name = os.path.join(dir_name, '%s.xml' % i)
        with open(file_name, mode='w', encoding='utf-8') as fp:
            fp.write(request)
        file_list.append(file_name)
    print('Подготовил для отправки %s файлов' % n)
    #exit(0)
    # Делаем отправку в несколько потоков

    for thread in (1, 3, 5, 7, 10, 12, 15, 20 , 25):
        start = time.time()
        pool = ThreadPool(thread)
        # Это многопоточная отправка
        pool.map(send_req, file_list)
        pool.close()
        pool.join()
        stop = time.time()
        print('Отправляли %s запросов в %s потоков' % (len(file_list), thread))
        print('потрачено времени %s сек' % (stop-start))
        print('общая скорость отправки - %s запросов в секунду' % (len(file_list)/(stop-start)))
        print('скорость в одном потоке - %s запросов в секунду' % (len(file_list)/(stop-start)/thread))
    exit(0)