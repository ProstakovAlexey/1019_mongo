# coding: utf8
import hashlib
import glob
import os
import random
import pprint

"""
Для проверки теории о том, что обращение к файловой системе может оказаться быстрее, чем обращение к БД и
проще в использовании для администратора без специальных знаний, я делаю аналог БД в ФС.
В качестве ключа буду использовать хеш от ФИО и ДР. Структура каталогов будет:
- data_1019 (каталог)
-- 4 первых символа (каталог)
--- остальные символы хеша (каталог)
---- дата_номер района.1019 - json файл с данными
Для генерации буду использовать созданные ранее файлы peoples
"""

payment_types = ('Единовременная выплата по рождению ребенка', 'Пособие по уходу за ребенком до 1.5 лет',
                 'Компенсация роста тарифов ЖКХ', 'Единовременная выплата в связи с ТЖС',
                 'Пособие по уходу за ребенком до 3-х лет', 'Ежемесячная выплата многодетнам семьям',
                 'Льгота на оплату ЖП и ЖКУ', 'Пособие по нуждаемости',
                 'Компенсания в связи с проживанием на загрязненной территории',
                 'Единовременная выплаты к праздничным датам')
# Кол-во выплат у каждого в месяц
payments = 3
# В скольких районах он будет стоять на учете
r = 2
pp = pprint.PrettyPrinter(indent=4,  width=150)

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


def payment_generate(path):
    """
    Создает файлы с выплатами по указанному пути. Имя файла = yyyy-mm-dd_raion.1019, структура json
    {
       doc: ,
       pays: [
         {
           pay: ,
           date: ,
           name: ,
         },
         ]
    }
    :param path: путь
    :return: кол-во созданых файлов
    """
    result = 0
    # Генерация выплаты
    year = '2017'
    months = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
    day = '01'
    sn = snils()
    # Создаем по районам
    for raion in ('1', '2'):
        # С вероятностью 1/100 у человека может сменится СНИЛС
        if random.randint(1, 100) == 7:
            sn = snils()
        # Создаю выплаты по месяцам
        for month in months:
            payments_list = list()
            # Создано выплат
            count_payments = 0
            while count_payments < payments:
                pay = random.randint(10000, 500000) / 100
                date = '{0}-{1}-{2}'.format(year, month, day)
                name = random.choice(payment_types)
                payments_list.append({'pay': pay, 'date': date, 'name': name})
                count_payments += 1
            # Добавляю район и его выплаты
            file_name = os.path.join(path, '{0}-{1}-{2}_{3}.1019'.format(year, month, day, raion))
            data = {'doc': sn, 'pays': payments_list}
            with open(file_name, mode='w', encoding='utf-8') as fp:
                fp.write(pp.pformat(data))
                result += 1
    return result


def get_hash(data):
    """
    Возвращает хэш от ФИО и ДР + соль
    :param data: строка вида Кузьмина;Наида;Тестович;23.01.1988
    :return:
    """
    fio_list = data.split(';')
    soul = 'Соцзащита1864io72grFG'
    # Нормализация ФИО и ДР
    fio = (fio_list[0]+fio_list[1]+fio_list[2]).upper() + fio_list[3] + soul
    # Хеш от ФИО и ДР
    fio = fio.encode('utf-8')
    return hashlib.sha256(fio).hexdigest()


def create_folder(directory):
    result = 0
    #print(directory)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            result = 1
    except OSError:
        print('Error: Creating directory. ' + directory)
    return result

example = 'peoples/*.txt'
result = 'data_1019'
# Получаем список всех файлов
file_list = glob.glob(example)
n = len(file_list)
i = 0
dir1 = 0
dir2 = 0
files = 0
for file_name in file_list:
    i += 1
    print('Обрабатываю файл {0} ({1} из {2})'.format(file_name, i, n))
    # Читаю файл построчно
    with open(file_name, mode='r', encoding='utf-8') as fp:
        for line in fp.readlines():
            # Получаю хеш от данных
            hash = get_hash(line.strip())
            # Создаю каталоги
            dir1 += create_folder(os.path.join(result, hash[0:4]))
            dir2 += create_folder(os.path.join(result, hash[0:4], hash[4:]))
            # Создаю файлы
            files += payment_generate(os.path.join(result, hash[0:4], hash[4:]))
            #break
    print('Создал каталогов 1-го уровня - {0}, второго уровна - {1}, файлов - {2}'.format(dir1, dir2, files))



