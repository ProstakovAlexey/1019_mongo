#!/usr/bin/python3
# -*- coding: utf-8 -*-
import falcon
import json
import function


class Static:
    """
    Выдает небольшую зашитую XML, нужно для проверки быстродействия сервиса
    """

    @staticmethod
    def on_post(req, resp):
        """Handles POST requests"""
        body = req.stream.read().decode('utf-8')
        resp.body = """
<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://socit.ru/message" xmlns:smev="http://smev.gosuslugi.ru/rev120315" xmlns:soc="http://socit.ru">
  <soapenv:Body>
    <mes:SocPaymentsTumenResponse>
      <smev:Message>
        <smev:Status>RESULT</smev:Status>
        <smev:Date>2018-06-05T10:43:45.403+03:00</smev:Date>
      </smev:Message>
      <smev:MessageData>
        <smev:AppData>
          <soc:Response>
            <soc:HasPayment>true</soc:HasPayment>
            <soc:Payments>
              <soc:Payment>
                <soc:Date>2017-11-01</soc:Date>
                <soc:Name>Назначение ежемесячной денежной компенсации,установленной частями 9,10 и 13 статьи 3 Федерального закона от 07.11.2011 № 306-ФЗ «О денежном довольствии военнослужащих и предоставлении им отдельных выплат»,военнослужащим,гражданам,призванным на военные сборы,и членам их семей,пенсионное обеспечение которых осуществляется ПФР,и членам их семей </soc:Name>
                <soc:Pay>17244.99</soc:Pay>
                <soc:Source>Тестовый район 2 (Простаков)</soc:Source>
              </soc:Payment>
            </soc:Payments>
          </soc:Response>
        </smev:AppData>
      </smev:MessageData>
    </mes:SocPaymentsTumenResponse>
  </soapenv:Body>
</soapenv:Envelope>
        """

    @staticmethod
    def on_get(req, resp):
        """Сервис не обслуживет get запросы, поэтому тут сообщение с ошибкой"""
        response = '''<h1>Ошибка!</h1>
        <p>Сервис принимает только POST запросы, в соответствии со своим описание</p>
        <p>Описание сервиса - http://109.195.183.171:2121/SocPortal/Help/SMEV_SERVICE_SOCPAYMENTSTUMEN.html</p>'''
        resp.body = json.dumps(response)


class Service1019:
    """
    Выдает результат с поиском в БД
    """

    @staticmethod
    def on_post(req, resp):
        """Handles POST requests"""
        body = req.stream.read().decode('utf-8')
        # Анализирует запрос, пытается найти там персональные данные
        people, err = function.analiz(body)
        if err:
            # Возникла ошибка, не удалось извлечь какие-то данные, выдаем сообщение об ошибке
            resp.body = function.error_resp(err)
        else:
            # Берем хэш
            hash = function.hash(people['FamilyName'], people['FirstName'], people['Patronymic'], people['BirthDate'])
            # Выполняем поиск в БД
            bd_result, err = function.find(hash, people['Snils'])
            if err:
                resp.body = function.error_resp(err)
            else:
                resp.body = function.ok_resp(bd_result)
        resp.append_header('Content-type', 'text/xml;charset="utf-8"')

    @staticmethod
    def on_get(req, resp):
        """Сервис не обслуживет get запросы, поэтому тут сообщение с ошибкой"""
        response = '''<h1>Ошибка!</h1>
        <p>Сервис принимает только POST запросы, в соответствии со своим описание</p>
        <p>Описание сервиса - http://109.195.183.171:2121/SocPortal/Help/SMEV_SERVICE_SOCPAYMENTSTUMEN.html</p>'''
        resp.body = json.dumps(response)


class Service1019a:
    """
    Выдает результат с поиском в файловой системе
    """

    @staticmethod
    def on_post(req, resp):
        """Handles POST requests"""
        body = req.stream.read().decode('utf-8')
        # Анализирует запрос, пытается найти там персональные данные
        people, err = function.analiz(body)
        if err:
            # Возникла ошибка, не удалось извлечь какие-то данные, выдаем сообщение об ошибке
            resp.body = function.error_resp(err)
        else:
            # Берем хэш
            hash = function.hash(people['FamilyName'], people['FirstName'], people['Patronymic'], people['BirthDate'])
            # Выполняем поиск в ФС
            result, err = function.find_json(hash)
            if err:
                resp.body = function.error_resp(err)
            else:
                resp.body = json.dumps(result)
        resp.append_header('Content-type', 'application/json; charset=utf-8')

    @staticmethod
    def on_get(req, resp):
        """Сервис не обслуживет get запросы, поэтому тут сообщение с ошибкой"""
        response = '''<h1>Ошибка!</h1>
        <p>Сервис принимает только POST запросы, в соответствии со своим описание</p>
        <p>выдает json<p>'''
        resp.body = json.dumps(response)


api = falcon.API()
api.add_route('/1019', Service1019())
api.add_route('/1019a', Service1019a())

api.add_route('/static', Static())
