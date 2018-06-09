# -*- coding: utf-8 -*-
__author__ = 'alexey'
import time
import sys
import random
import urllib.request
import urllib.error
from xml.dom.minidom import *
import hashlib



def get_wsdl(IS, url, name='wsdl.wsdl'):
    '''Получает WSDL и пишет его в файл'''
    addr = 'http://%s:%s%s?wsdl' % (IS['adr'], IS['port'], url)
    err = 0
    file_name = 'Результаты/'+name
    try:
        response = urllib.request.urlopen(addr)
    except urllib.error.HTTPError:
        print ('При получении WSDL возникли ошибки! Не удалось обратится по адресу:', addr)
        err += 1
    else:
        print('WSDL успешно получена по адресу:', addr)
        wsdl = response.read().decode('utf-8')
        # убираем двойной перевод строки
        wsdl = wsdl.replace('\r\n', '\n')
        with open(file_name, mode="w", encoding="utf-8") as fp:
            fp.write(wsdl)
    return err


def snils(init=0):
    """ Функция генерирует СНИСЛ, начинающийся с 002 (чтобы легче было искать) остальные
    числа случайные, контрольное число вычисляется
    Страховой номер индивидуального лицевого счета страхового свидетельства обязательного пенсионного страхования(он же СНИЛС) проверяется на валидность контрольным числом. СНИЛС имеет вид: «XXX-XXX-XXX YY», где XXX-XXX-XXX — собственно номер, а YY — контрольное число. Алгоритм формирования контрольного числа СНИЛС таков:
    1) Проверка контрольного числа Страхового номера проводится только для номеров больше номера 001-001-998
    2) Контрольное число СНИЛС рассчитывается следующим образом:
    2.1) Каждая цифра СНИЛС умножается на номер своей позиции (позиции отсчитываются с конца)
    2.2) Полученные произведения суммируются
    2.3) Если сумма меньше 100, то контрольное число равно самой сумме
    2.4) Если сумма равна 100 или 101, то контрольное число равно 00
    2.5) Если сумма больше 101, то сумма делится по остатку на 101 и контрольное число определяется остатком от деления аналогично пунктам 2.3 и 2.4
    ПРИМЕР: Указан СНИЛС 112-233-445 95
    Проверяем правильность контрольного числа:
    цифры номера        1 1 2 2 3 3 4 4 5
    номер позиции       9 8 7 6 5 4 3 2 1
    Сумма = 1×9 + 1×8 + 2×7 + 2×6 + 3×5 + 3×4 + 4×3 + 4×2 + 5×1 = 95
    95 ÷ 101 = 0, остаток 95.
    Контрольное число 95 — указано верно """
    if init != 0:
        random.seed(init)
    # заполняем начальные числа СНИСЛ
    arr = [0, 0, 2]
    # res - переменная для результата
    res = ""
    contr = 0
    for i in range(3, 9):
        arr.append(random.randint(0, 9))
    for i in range(0, 9):
        contr += arr[i] * (9 - i)
        res += str(arr[i])
    if contr > 99:
        if contr == 100 or contr == 101:
            contr = 0
        else:
            contr %= 101
    if contr < 10:
        res += "0" + str(contr)
    else:
        res += str(contr)
    return res


def get_smev_date():
    """ Возвращает текущую дату, в формате СМЭВ """
    # возвращает текущее время в struct_time
    now = time.localtime()
    # форматирование к виду 2014-01-16T14:51:45.566+04:00
    return time.strftime("%Y-%m-%dT%H:%M:%S+03:00", now)


def case_num(n=6, init=0):
    '''Возвращает случайный номер состоящий из n цифр'''
    if init != 0:
        random.seed(init)
    result = ''
    for i in range(0, n):
        s = random.randint(0, 9)
        result += str(s)
    return result


def change(s, IS):
    """Проводит замены в строке, возвращает готовую
    s: входная строка
    IS: сведения об ИС Наименование, Мнемоника, ОКТМО (словарь)
    """
    s = s.replace('#VERSION#', 'rev120315')
    s = s.replace('#SERVICE_MNEMONIC#', 'TestMnemonic')
    s = s.replace('#SERVICE_VERSION#', '2.01')
    for key in IS.keys():
        # все символы делает заглавными и решетки
        st = "#%s#" % key.upper()
        s = s.replace(st, IS[key])
    s = s.replace('#DATE#', get_smev_date())
    return s


def check(req, name, contr):
    """
    :param req: XML текст
    :param sum: контрольная сумма
    :return: 1 - ошибка, 0 - ок.
    """
    err = 1
    i = req.find('<smev:MessageData>')
    if i > 0:
        # блок с ответом найден
        summ = hashlib.md5(req[i:].encode())
        if contr == summ.hexdigest():
            err = 0
        else:
            print("Контрольная сумма для %s=%s" % (name, summ.hexdigest()))
    return err


def write_file(s, metod, code=None):
    """ Записывает файл. Вход - имя строка для записи в файл и префикс"""
    err = 0

    try:
        file_name = parseString(s).getElementsByTagName('smev:Status')[0]
        file_name = file_name.firstChild.nodeValue
    except:
        try:
            file_name = parseString(s).getElementsByTagName('rev:Status')[0]
            file_name = file_name.firstChild.nodeValue
        except:
            Type, Value, Trace = sys.exc_info()
            file_name = "FAULT"
            print("Не удалось распарсить файл. Вероятно xml структура повреждена. Файл будет сохранен как %s, выполнение продолжено" % (file_name))
            print("Ошибка Тип:", Type, "Значение:", Value)
            err += 1
    if code:
        file_name = 'Результаты/%s(%s)_%s.xml' % (metod, code, file_name)
    else:
        file_name = 'Результаты/'+metod+'_'+file_name+'.xml'
    # добавляем строку с кодировкой если ее нет
    if s.startswith('<?xml version="1.0" encoding="utf-8"?>') == False:
        s = '<?xml version="1.0" encoding="utf-8"?>\n'+s
    with open(file_name, mode="w", encoding="utf-8") as fp:
        fp.write(s)
    return err
