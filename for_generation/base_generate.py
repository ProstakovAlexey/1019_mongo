# coding: utf8
__author__ = 'Prostakov Alexey'
#import datetime
from pymongo import MongoClient
import pprint
from elizabeth import Personal
from elizabeth import Generic
import random
import hashlib
import datetime
import time

"""Заполняет БД сгенированными людьми. ФИО, ДР берет из Элизабет,
выплаты делает на основании списка выплат. Делает 3 млн ПКУ, 120 млн.
выплат за 1 год (10 записей в месяц)
"""
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
    if init !=0:
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


raions = ('Алексинский район', 'Арсеньевский район', 'Белёвский район', 'Богородицкий район', 'Венёвский район',
          'Воловский район', 'Дубенский район', 'Ефремовский район', 'Заокский район',
          'Каменский район', 'Кимовский район', 'Киреевский район', 'Куркинский район',
          'Ленинский район', 'Новомосковский район', 'Одоевский район', 'Плавский район', 'Суворовский район',
          'Тёпло-Огарёвский район', 'Узловский район', 'Чернский район', 'Щёкинский район',
          'Ясногорский район')
payment_types = ('Единовременная выплата по рождению ребенка', 'Пособие по уходу за ребенком до 1.5 лет',
                 'Компенсация роста тарифов ЖКХ', 'Единовременная выплата в связи с ТЖС',
                 'Пособие по уходу за ребенком до 3-х лет', 'Ежемесячная выплата многодетнам семьям',
                 'Льгота на оплату ЖП и ЖКУ', 'Пособие по нуждаемости',
                 'Компенсания в связи с проживанием на загрязненной территории',
                 'Единовременная выплаты к праздничным датам')
pp = pprint.PrettyPrinter(indent=4)

# Кол-во выплат у каждого
payments = 10
# В скольких районах он будет стоять на учете
r = 2
# Соль
soul = 'Соцзащита1864io72grFG'
# Настройка генератора на Елизабет
g = Generic('ru')
user = Personal('ru')
pols = ('male', 'female')

# Соединение с БД
client = MongoClient('192.168.0.195', 27017)
db = client['1019']
collection = db['payments']
# Кол-во упаковок
packs = 300
pack_count = 0

while pack_count < packs:
    pack_count += 1
    start = time.time()
    people_for_download = dict()
    # Кол-во людей, которых надо сгенерировать
    peoples = 10000
    # Уже сделано
    count_peoples = 0
    # Записать в файлик
    fp = open('people_%s.txt' % pack_count, encoding='utf-8', mode='a')
    while count_peoples < peoples:
        # Генерируем ФИО и ДР
        sex = random.choice(pols)
        p_famil = user.surname(gender=sex)
        p_name = user.name(gender=sex)
        p_otch = 'Тестович'
        if sex == 'female':
            p_otch = 'Тестовна'
        p_dr = g.datetime.date(start=1970, end=2000)
        fio = p_famil+p_name+p_otch+p_dr
        # Нормализация ФИО и ДР
        fio = fio.upper()+soul
        # Хеш от ФИО и ДР
        bin = fio.encode('utf-8')
        hash = hashlib.sha256(bin).hexdigest()
        sn = snils()
        r_count = 0
        citizen = {
            'key': hash,
            'dep': dict()
        }
        while r_count < r:
            # Генерация выплаты
            count_payments = 0
            payments_dict = dict()
            # С вероятностью 1/100 у человека может сменится СНИЛС
            if random.randint(1, 100) == 7:
                sn = snils()
            # Выбираем район
            raion = random.choice(raions)
            # Добавляем ему выплаты
            payments_list = list()
            while count_payments < payments:
                pay = random.randint(10000, 500000)/100
                date = datetime.datetime(year=2017, month=random.randint(1, 12), day=random.randint(1, 27))
                name = random.choice(payment_types)
                payments_list.append({'pay': pay, 'date': date, 'name': name})
                count_payments += 1
            # Добавляю район и его выплаты
            citizen['dep'][raion] = {'doc': sn, 'pays': payments_list}
            r_count += 1
        count_peoples += 1
        #pp.pprint(citizen)
        people_for_download = citizen['dep']
        people_for_download['_id'] = citizen['key']
        #pp.pprint(people_for_download)
        # Запись в БД
        print('%s;%s;%s;%s' % (p_famil, p_name, p_otch, p_dr), file=fp)
        try:
            collection.insert(people_for_download)
        except :
            print('Двойной ключ')

    fp.close()
    print('Запись упаковки №%s, заняло %s сек' % (pack_count, time.time() - start))
client.close()

