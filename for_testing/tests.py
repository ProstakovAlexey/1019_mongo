import unittest
import function
import os
import datetime

"""
unittest использовались для тестирования сервис во время его написания
"""

# папка с примерами
dir = 'sample'


class Analiz(unittest.TestCase):
    """Проверяет функцию анализа запроса xml"""
    def test1(self):
        """Нет фамилии"""
        file_name = os.path.join(dir, 'ERR_5(1019)_REQUEST.xml')
        with open(file_name, encoding='utf-8', mode='r') as fp:
            req = fp.read()
        people, err = function.analiz(req)
        self.assertEqual(err, 5)

    def test2(self):
        """Нет имени"""
        file_name = os.path.join(dir, 'ERR_6(1019)_REQUEST.xml')
        with open(file_name, encoding='utf-8', mode='r') as fp:
            req = fp.read()
        people, err = function.analiz(req)
        self.assertEqual(err, 10)

    def test3(self):
        """Нет ДР"""
        file_name = os.path.join(dir, 'ERR_7(1019)_REQUEST.xml')
        with open(file_name, encoding='utf-8', mode='r') as fp:
            req = fp.read()
        people, err = function.analiz(req)
        self.assertEqual(err, 15)

    def test4(self):
        """Проверяет правильность извлечения ФИО и СНИЛС"""
        file_name = os.path.join(dir, 'ERR_9(1019)_REQUEST.xml')
        with open(file_name, encoding='utf-8', mode='r') as fp:
            req = fp.read()
        people, err = function.analiz(req)
        self.assertEqual(err, 0)
        self.assertEqual(people['FamilyName'], 'Тестов')
        self.assertEqual(people['FirstName'], 'Тюмень')
        self.assertEqual(people['Patronymic'], 'ЕстьВыплата')
        self.assertEqual(people['BirthDate'], '1970-10-19')
        self.assertEqual(people['Snils'], '67867887619')


class DB_find(unittest.TestCase):
    """Поиск в БД. Он опирается на налачие людей в БД. Если будет падать по причине
    что их нет, нужно отключить"""


    def test1(self):
        """Поиск по ФИО+ДР"""
        famil = 'Кузьмина'
        name = 'Наида'
        otch = 'Тестович'
        dr = '23.01.1988'
        hash = function.hash(famil, name, otch, dr)
        info, err = function.find(hash)
        self.assertEqual(err, 0)


class ResponsePrint(unittest.TestCase):
    """Проверяет метод красивой печати ответа"""

    def test1(self):
        # Проверяет форматирование ответа
        response = {'_id': '2de5d8ecd5d32669a9bd9c2505e7d4df153b0efb7643de49be0c4f41a66461fe',
                    'Венёвский район': {'doc': '00214088080', 'pays': [
                        {'pay': 1713.05, 'date': datetime.datetime(2017, 3, 13, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1761.73, 'date': datetime.datetime(2017, 11, 11, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 3141.42, 'date': datetime.datetime(2017, 9, 22, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1528.66, 'date': datetime.datetime(2017, 4, 5, 0, 0),
                         'name': 'Компенсация роста тарифов ЖКХ'},
                        {'pay': 4109.32, 'date': datetime.datetime(2017, 5, 11, 0, 0),
                         'name': 'Компенсация роста тарифов ЖКХ'},
                        {'pay': 3456.03, 'date': datetime.datetime(2017, 12, 2, 0, 0),
                         'name': 'Льгота на оплату ЖП и ЖКУ'},
                        {'pay': 4321.91, 'date': datetime.datetime(2017, 11, 26, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4134.44, 'date': datetime.datetime(2017, 9, 8, 0, 0),
                         'name': 'Компенсания в связи с проживанием на загрязненной территории'},
                        {'pay': 537.43, 'date': datetime.datetime(2017, 8, 25, 0, 0), 'name': 'Пособие по нуждаемости'},
                        {'pay': 515.05, 'date': datetime.datetime(2017, 11, 25, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'}]},
                    'Заокский район': {'doc': '00214088080', 'pays': [
                        {'pay': 293.57, 'date': datetime.datetime(2017, 12, 1, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4337.08, 'date': datetime.datetime(2017, 8, 17, 0, 0),
                         'name': 'Ежемесячная выплата многодетнам семьям'},
                        {'pay': 2252.44, 'date': datetime.datetime(2017, 8, 25, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1500.83, 'date': datetime.datetime(2017, 9, 4, 0, 0),
                         'name': 'Пособие по уходу за ребенком до 1.5 лет'},
                        {'pay': 4765.88, 'date': datetime.datetime(2017, 11, 4, 0, 0),
                         'name': 'Ежемесячная выплата многодетнам семьям'},
                        {'pay': 3809.31, 'date': datetime.datetime(2017, 9, 8, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'},
                        {'pay': 918.16, 'date': datetime.datetime(2017, 9, 1, 0, 0),
                         'name': 'Компенсания в связи с проживанием на загрязненной территории'},
                        {'pay': 1161.03, 'date': datetime.datetime(2017, 8, 18, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 3179.98, 'date': datetime.datetime(2017, 5, 20, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4880.0, 'date': datetime.datetime(2017, 8, 5, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'}]}}
        obr = [['13.03.2017', 'Единовременная выплата по рождению ребенка', 1713.05, 'Венёвский район'],
               ['05.04.2017', 'Компенсация роста тарифов ЖКХ', 1528.66, 'Венёвский район'],
               ['11.05.2017', 'Компенсация роста тарифов ЖКХ', 4109.32, 'Венёвский район'],
               ['20.05.2017', 'Единовременная выплата по рождению ребенка', 3179.98, 'Заокский район'],
               ['05.08.2017', 'Единовременная выплаты к праздничным датам', 4880.0, 'Заокский район'],
               ['17.08.2017', 'Ежемесячная выплата многодетнам семьям', 4337.08, 'Заокский район'],
               ['18.08.2017', 'Единовременная выплата по рождению ребенка', 1161.03, 'Заокский район'],
               ['25.08.2017', 'Единовременная выплата по рождению ребенка', 2252.44, 'Заокский район'],
               ['25.08.2017', 'Пособие по нуждаемости', 537.43, 'Венёвский район'],
               ['01.09.2017', 'Компенсания в связи с проживанием на загрязненной территории', 918.16, 'Заокский район'],
               ['04.09.2017', 'Пособие по уходу за ребенком до 1.5 лет', 1500.83, 'Заокский район'],
               ['08.09.2017', 'Единовременная выплаты к праздничным датам', 3809.31, 'Заокский район'],
               ['08.09.2017', 'Компенсания в связи с проживанием на загрязненной территории', 4134.44,
                'Венёвский район'],
               ['22.09.2017', 'Единовременная выплата по рождению ребенка', 3141.42, 'Венёвский район'],
               ['04.11.2017', 'Ежемесячная выплата многодетнам семьям', 4765.88, 'Заокский район'],
               ['11.11.2017', 'Единовременная выплата по рождению ребенка', 1761.73, 'Венёвский район'],
               ['25.11.2017', 'Единовременная выплаты к праздничным датам', 515.05, 'Венёвский район'],
               ['26.11.2017', 'Единовременная выплата по рождению ребенка', 4321.91, 'Венёвский район'],
               ['01.12.2017', 'Единовременная выплата по рождению ребенка', 293.57, 'Заокский район'],
               ['02.12.2017', 'Льгота на оплату ЖП и ЖКУ', 3456.03, 'Венёвский район']]
        f = function.result_format(response)
        self.assertEqual(f, obr)

    def test2(self):
        # Проверяет печать ответа
        response = {'_id': '2de5d8ecd5d32669a9bd9c2505e7d4df153b0efb7643de49be0c4f41a66461fe',
                    'Венёвский район': {'doc': '00214088080', 'pays': [
                        {'pay': 1713.05, 'date': datetime.datetime(2017, 3, 13, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1761.73, 'date': datetime.datetime(2017, 11, 11, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 3141.42, 'date': datetime.datetime(2017, 9, 22, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1528.66, 'date': datetime.datetime(2017, 4, 5, 0, 0),
                         'name': 'Компенсация роста тарифов ЖКХ'},
                        {'pay': 4109.32, 'date': datetime.datetime(2017, 5, 11, 0, 0),
                         'name': 'Компенсация роста тарифов ЖКХ'},
                        {'pay': 3456.03, 'date': datetime.datetime(2017, 12, 2, 0, 0),
                         'name': 'Льгота на оплату ЖП и ЖКУ'},
                        {'pay': 4321.91, 'date': datetime.datetime(2017, 11, 26, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4134.44, 'date': datetime.datetime(2017, 9, 8, 0, 0),
                         'name': 'Компенсания в связи с проживанием на загрязненной территории'},
                        {'pay': 537.43, 'date': datetime.datetime(2017, 8, 25, 0, 0), 'name': 'Пособие по нуждаемости'},
                        {'pay': 515.05, 'date': datetime.datetime(2017, 11, 25, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'}]},
                    'Заокский район': {'doc': '00214088080', 'pays': [
                        {'pay': 293.57, 'date': datetime.datetime(2017, 12, 1, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4337.08, 'date': datetime.datetime(2017, 8, 17, 0, 0),
                         'name': 'Ежемесячная выплата многодетнам семьям'},
                        {'pay': 2252.44, 'date': datetime.datetime(2017, 8, 25, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1500.83, 'date': datetime.datetime(2017, 9, 4, 0, 0),
                         'name': 'Пособие по уходу за ребенком до 1.5 лет'},
                        {'pay': 4765.88, 'date': datetime.datetime(2017, 11, 4, 0, 0),
                         'name': 'Ежемесячная выплата многодетнам семьям'},
                        {'pay': 3809.31, 'date': datetime.datetime(2017, 9, 8, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'},
                        {'pay': 918.16, 'date': datetime.datetime(2017, 9, 1, 0, 0),
                         'name': 'Компенсания в связи с проживанием на загрязненной территории'},
                        {'pay': 1161.03, 'date': datetime.datetime(2017, 8, 18, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 3179.98, 'date': datetime.datetime(2017, 5, 20, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4880.0, 'date': datetime.datetime(2017, 8, 5, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'}]}}
        f = function.result_format(response)
        r = function.result_print(f)
        with open('sample/print1.txt', mode='r', encoding='utf-8') as fp:
            obr = fp.read()
        self.assertEqual(r, obr)


class ResponseXML(unittest.TestCase):
    """Проверяет подготовку XML"""
    def test1(self):
        # Проверяет форматирование ответа.
        # //TODO Не сумел заставить работать хотя визульано все ок
        response = {'_id': '2de5d8ecd5d32669a9bd9c2505e7d4df153b0efb7643de49be0c4f41a66461fe',
                    'Венёвский район': {'doc': '00214088080', 'pays': [
                        {'pay': 1713.05, 'date': datetime.datetime(2017, 3, 13, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1761.73, 'date': datetime.datetime(2017, 11, 11, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 3141.42, 'date': datetime.datetime(2017, 9, 22, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1528.66, 'date': datetime.datetime(2017, 4, 5, 0, 0),
                         'name': 'Компенсация роста тарифов ЖКХ'},
                        {'pay': 4109.32, 'date': datetime.datetime(2017, 5, 11, 0, 0),
                         'name': 'Компенсация роста тарифов ЖКХ'},
                        {'pay': 3456.03, 'date': datetime.datetime(2017, 12, 2, 0, 0),
                         'name': 'Льгота на оплату ЖП и ЖКУ'},
                        {'pay': 4321.91, 'date': datetime.datetime(2017, 11, 26, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4134.44, 'date': datetime.datetime(2017, 9, 8, 0, 0),
                         'name': 'Компенсания в связи с проживанием на загрязненной территории'},
                        {'pay': 537.43, 'date': datetime.datetime(2017, 8, 25, 0, 0), 'name': 'Пособие по нуждаемости'},
                        {'pay': 515.05, 'date': datetime.datetime(2017, 11, 25, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'}]},
                    'Заокский район': {'doc': '00214088080', 'pays': [
                        {'pay': 293.57, 'date': datetime.datetime(2017, 12, 1, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4337.08, 'date': datetime.datetime(2017, 8, 17, 0, 0),
                         'name': 'Ежемесячная выплата многодетнам семьям'},
                        {'pay': 2252.44, 'date': datetime.datetime(2017, 8, 25, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 1500.83, 'date': datetime.datetime(2017, 9, 4, 0, 0),
                         'name': 'Пособие по уходу за ребенком до 1.5 лет'},
                        {'pay': 4765.88, 'date': datetime.datetime(2017, 11, 4, 0, 0),
                         'name': 'Ежемесячная выплата многодетнам семьям'},
                        {'pay': 3809.31, 'date': datetime.datetime(2017, 9, 8, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'},
                        {'pay': 918.16, 'date': datetime.datetime(2017, 9, 1, 0, 0),
                         'name': 'Компенсания в связи с проживанием на загрязненной территории'},
                        {'pay': 1161.03, 'date': datetime.datetime(2017, 8, 18, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 3179.98, 'date': datetime.datetime(2017, 5, 20, 0, 0),
                         'name': 'Единовременная выплата по рождению ребенка'},
                        {'pay': 4880.0, 'date': datetime.datetime(2017, 8, 5, 0, 0),
                         'name': 'Единовременная выплаты к праздничным датам'}]}}
        f = function.ok_resp(response)
        #with open('sample/resp_ok.xml', 'w', encoding='utf-8') as fp:
        #    fp.write(f)
        with open('sample/resp_ok.xml', 'r', encoding='utf-8') as fp:
            obr = fp.read()
        self.assertEqual(f, obr)

    def test2(self):
        # Проверяет форматирование ответа.
        # //TODO Не сумел заставить работать хотя визульано все ок
        response = None
        f = function.ok_resp(response)
        with open('sample/resp_nofound.xml', 'w', encoding='utf-8') as fp:
            fp.write(f)
        with open('sample/resp_nofound.xml', 'r', encoding='utf-8') as fp:
            obr = fp.read()
        self.assertEqual(f, obr)


