import hashlib
import xml.etree.ElementTree as etree
import uuid
import datetime
from pymongo import MongoClient

# Прочитываем шаблоны сообщений
with open('shablons/1019_err.xml', encoding='utf-8') as fp:
    err_shablon = fp.read()
with open('shablons/1019_ok.xml', encoding='utf-8') as fp:
    ok_shablon = fp.read()
with open('shablons/1019_nofound.xml', encoding='utf-8') as fp:
    nofound_shablon = fp.read()
# Сообщения об ошибках
err_message = {5: 'Не указана фамилия', 10: 'Не указано имя', 15: 'Не дата рождения', 99: 'Ошибка БД'}
# Соединение с БД
client = MongoClient('192.168.0.195', 27017)
db = client['1019']
collection = db['payments']


def hash(famil, name, otch, bithday):
    """
    По персональным данным человека выдает хэш
    :param famil: фамилия
    :param name: имя
    :param otch: отчество
    :param bithday: датарождения
    :return: хеш
    """
    soul = 'Соцзащита1864io72grFG'
    fio = famil + name + otch + bithday
    # Нормализация ФИО и ДР
    fio = fio.upper() + soul
    # Хеш от ФИО и ДР
    bin = fio.encode('utf-8')
    return hashlib.sha256(bin).hexdigest()


def find(hash, docum=None):
    """
    Поиск в БД по хэшу и уточняет результат по документу (СНИЛС например)
    :param hash:
    :return:
    """
    err = 0
    info = None
    try:
        info = collection.find_one({'_id': hash})
    except:
        err = 99
    return info, err


def smev_change(xml):
    """Заполняет поля в обертке СМЭВ"""
    # //TODO надо не генерировать OriginalRequest, а получать его из запроса
    smev = {'SenderCode': 'АСП_01', 'SenderName': 'Поставщик',
            'RecipientCode': 'RPGU_01', 'RecipientName': 'Потребитель',
            'RequestId': str(uuid.uuid1()), 'OriginalRequest': str(uuid.uuid1()),
            'Date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000+3:00')
    }
    return xml.format(**smev)


def error_resp(err_code):
    """По коду ошибки выдает XML с сообщением об ошибке
    :param err_code: код ошибки
    :return: готовая к отправке XML
    """
    err = {'ErrorCode': err_code}
    if err_code in err_message:
        err['ErrorMessage'] = err_message[err_code]
    else:
        err['ErrorMessage'] = 'Нет сообщения об ошибке'
    message = err_shablon.format(**err)
    return smev_change(message)


def analiz(request):
    """По тексту XML ищет персональные данные человека, если не находит возвращает код ошибки
    :param request: xml текст запроса
    :return: персданные и код ошибки
    """
    err_code = 0
    tree = etree.fromstring(request)
    req = tree.find(
        '{http://schemas.xmlsoap.org/soap/envelope/}Body/'
        '{http://socit.ru/message}SocPaymentsTumenRequest/'
        '{http://smev.gosuslugi.ru/rev120315}MessageData/'
        '{http://smev.gosuslugi.ru/rev120315}AppData/'
        '{http://socit.ru}Request')
    find_list = (('FamilyName', 5), ('FirstName', 10), ('BirthDate', 15))
    people = dict()
    for i in find_list:
        try:
            people[i[0]] = req.find('{http://socit.ru}%s' % i[0]).text.strip()
        except AttributeError:
            err_code = i[1]
            break
    # Возможно передали СНИЛС
    try:
        sn = req.find('{http://socit.ru}Snils').text.strip()
        # Удалим все не цифровые символы
        snils = ''
        for j in sn:
            if j.isdigit():
                snils += j
        people['Snils'] = snils
    except AttributeError:
        people['Snils'] = None
    # Отчество, его может не быть. В таком случае считаем что его у человека нет
    try:
        people['Patronymic'] = req.find('{http://socit.ru}Patronymic').text.strip()
    except AttributeError:
        people['Patronymic'] = ''
    return people, err_code


def result_format(response):
    """
    Преобразует формат ответа к виду пригодному для ответа сервиса
    :param response: словарь
    :return: строка
    """
    # На первом уровне лежат id и названия районов
    payments = list()
    # 0 - дата, 1 - наименование, 2 сумма, 3 район
    for key1 in response.keys():
        if key1 == '_id':
            # Это не район, переходим к следующему
            continue
        # Район нашли
        raion = key1
        for pay in response[raion]['pays']:
            payments.append([pay['date'], pay['name'], pay['pay'], raion])
    # Сортируем список выплат
    payments.sort()
    # Преобразуем формат даты в строку
    for p in payments:
        p[0] = p[0].strftime('%d.%m.%Y')
    return payments


def result_print(result_list):
    """Выдает строку для красивой печати результаты выплаты.
    :param result_list: форматированныя список выплат
    :return:
    """
    s = ''
    for i in result_list:
        s += '{0}\t{1}\t{2}\t{3}\n'.format(*i)
    #with open('sample/print1.txt', mode='w', encoding='utf-8') as fp:
    #    fp.write(s)
    return s


def ok_resp(resp):
    """
    Выдает готовую xml для отправки в СМЭВ по ответу из БД
    :param resp:
    :return:
    """
    # Ответ из БД не пустой
    if resp:
        # Преобразовать ответ из БД у добный формат
        sh = '''                <soc:Payment>
                    <soc:Date>{}</soc:Date>
                    <soc:Name>{}</soc:Name>
                    <soc:Pay>{}</soc:Pay>
                    <soc:Source>{}</soc:Source>
                </soc:Payment>
'''
        s = ''
        for i in result_format(resp):
            s += sh.format(*i)
        return smev_change(ok_shablon.replace('{Payments}', s))
    # Пустой
    else:
        return smev_change(nofound_shablon)










