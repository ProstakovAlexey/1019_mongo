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
Изменение скорости отправки запросов с учетом только web части
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


xml = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:smev="http://smev.gosuslugi.ru/rev120315" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:mes="http://socit.ru/message" xmlns:soc="http://socit.ru">
   <soap:Body wsu:Id="body">
      <mes:SocPaymentsTumenRequest>
         <smev:Message>
            <smev:Sender>
               <smev:Code>SOCP01711</smev:Code>
               <smev:Name>СОЦИНФОРМТЕХ</smev:Name>
            </smev:Sender>
            <smev:Recipient>
               <smev:Code>SOCP01711</smev:Code>
               <smev:Name>СОЦИНФОРМТЕХ</smev:Name>
            </smev:Recipient>
            <smev:Originator>
               <smev:Code>SOCP01711</smev:Code>
               <smev:Name>СОЦИНФОРМТЕХ</smev:Name>
            </smev:Originator>
            <smev:ServiceName>TestMnemonic</smev:ServiceName>
            <smev:TypeCode>GSRV</smev:TypeCode>
            <smev:Status>REQUEST</smev:Status>
            <smev:Date>2018-06-07T15:20:33+03:00</smev:Date>
            <smev:ExchangeType>2</smev:ExchangeType>
            <smev:TestMsg>Test</smev:TestMsg>
            <smev:OKTMO>70000000</smev:OKTMO>
         </smev:Message>
         <smev:MessageData>
            <smev:AppData>
               <soc:Request>
	              <soc:FamilyName>Орехов</soc:FamilyName>
                  <soc:FirstName>Авксентий</soc:FirstName>
                  <soc:Patronymic>Тестович</soc:Patronymic>
                  <soc:BirthDate>10.09.1985</soc:BirthDate>
                  <soc:Snils>11122233344</soc:Snils>
               </soc:Request>
            </smev:AppData>
         </smev:MessageData>
      </mes:SocPaymentsTumenRequest>
   </soap:Body>
</soap:Envelope>
"""


def send_req(numer):
    con = http.client.HTTPConnection(TI['adr'], TI['port'])
    # Пытаемся отправить 1-ю часть
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    try:
        con.request("POST", TI['url'], xml.encode('utf-8'), headers=headers)
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
    n = 10000
    file_list = list()
    for i in range(0, n):
        file_list.append(i)
    print('Подготовил для отправки %s примеров' % n)
    #exit(0)
    # Делаем отправку в несколько потоков

    for thread in (1, 3, 5, 7, 10, 12, 15, 20, 25):
        start = time.time()
        pool = ThreadPool(thread)
        # Это многопоточная отправка
        results = (pool.map(send_req, file_list))
        pool.close()
        pool.join()
        stop = time.time()
        print('Отправляли %s запросов в %s потоков' % (len(file_list), thread))
        print('потрачено времени %s сек' % (stop-start))
        print('общая скорость отправки - %s запросов в секунду' % (len(file_list)/(stop-start)))
        print('скорость в одном потоке - %s запросов в секунду' % (len(file_list)/(stop-start)/thread))
    exit(0)
