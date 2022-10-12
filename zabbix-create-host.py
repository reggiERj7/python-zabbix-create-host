# -*- coding: utf-8 -*-
from itertools import count
from pyzabbix import ZabbixAPI

# Авторизация в Zabbix
zapi = ZabbixAPI("http://zabbix.kbsu/zabbix")
zapi.login(user="Admin", password="zabbix")

def main():
		count = 0
	 # открытие файла с адресами (данными)
    with open("addreses.txt", "r") as file:
        for i in file:
						# Пребразование строки с данными в массив
            data = i.split(".")
						# Парсинг номера хоста (последний октет) из данных
            workplace = data[3].replace("\n", "")
						# Парсинг номера аудитории (последний октет) из данных
            auditoria = data[4].replace("\n", "")
						# Парсинг ip-адреса из данных 
            ip = f'{data[0]}.{data[1]}.{data[2]}.{data[3]}'
						# Проверка валидности данных и пуш данных в Zabbix
            try:
                zapi.host.create(
                    host = f"a{auditoria}w{workplace}",
                    status= 0,
                    available = 1,
                    interfaces=[{
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "port": 10050,
                        "dns": ""
                    }],
                    groups=[{
												# Меняется в зависимости от подключемой группы узлов
                        "groupid": 38
                    }],
                    templates=[{
												# Меняется в зависимости от подключаемого шаблона элементов 
                        "templateid": 10574
                    }])
								count += 1
								print(f'{[count]} Хост: a{auditoria}w{workplace} с адресом - {ip} внесен')
            except:
								print(f'Произошла ошибка с внесением хоста: a{auditoria}w{workplace} с адресом - {ip} внесен. Возможно такой хост уже существует в системе...')
                continue
		print(f'Было внесено {count} хоста(-ов)')


main()