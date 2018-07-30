import http.client
import sys
import time

from for_testing import smev

"""
Нужна для проверки работы сервиса. Отправляет одиночный запрос, печатает ответ.
Куда отправлять, нужно указать ниже
"""

dir_name = 'for_test'
# Куда отправлять
TI = dict()
TI['snd_name'] = 'СОЦИНФОРМТЕХ'
TI['snd_code'] = 'SOCP01711'
TI['oktmo'] = '70000000'
# Выборка из mongodb
#TI['url'] = '/1019'
# Выборка из ФС
#TI['url'] = '/1019a'
# Получить статичный ответ
TI['url'] = '/static'
TI['adr'] = 'ti'
TI['port'] = '80'
TI['servicecode'] = '123456789'

# Выполнил подготовку
with open('shablons/Request_1019.xml', mode='r', encoding='utf-8') as fp:
    shablon = fp.read()
# Подменить стандарные поля СМЭВ
shablon = smev.change(shablon, TI)


def send_req(people):
    # Создать запрос на основе шаблона и словаря с параметрами
    con = http.client.HTTPConnection(TI['adr'], TI['port'])
    # Соединяется с веб-сервисом, игнорировать проблему с сертификатом
    #con = http.client.HTTPSConnection(TI['adr'], TI['port'], context=ssl._create_unverified_context())
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    request = shablon.format(**people)
    result = None
    try:
        con.request("POST", TI['url'], request.encode('utf-8'), headers=headers)
        result = con.getresponse().read()
        result = result.decode('utf-8')
        print(result)
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
    # Заполняю список тестового человека
    people = dict()
    people['FamilyName'] = 'Кузьмина'
    people['FirstName'] = 'Наида'
    people['Patronymic'] = 'Тестович'
    people['BirthDate'] = '23.01.1988'
    people['Snils'] = '11122233344'
    print('Начинаю отправку')
    start = time.time()
    send_req(people)
    stop = time.time()
    print('потрачено времени %s сек' % (stop-start))
    exit(0)
