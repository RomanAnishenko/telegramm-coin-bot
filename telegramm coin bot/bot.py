from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from telethon import TelegramClient, events, sync
import requests
import json
import hashlib
from time import sleep, time
import re
import webbrowser
import urllib.request
import os
import sqlite3
import collections
import random
import string
import datetime
import sys
import log



def no_task(x, cur, opts, client, driver, time_list, earnings_list, cycles_passed, start_time):

    print('Заданий больше нет. Бот ожидает заданние')
    driver.quit()
    d = datetime.date(2020, 1, 20)

    if len(time_list) > 0 and len(earnings_list) > 0 and cycles_passed > 0:
        average_time = sum(time_list) / len(time_list)
        average_balance = sum(earnings_list) / len(earnings_list)

        print('Всего пройденно циклов: ' + str(cycles_passed) + '\nСреднее время цикла: ' + str(average_time) + " \nЗаработанно: " + str(average_balance))
        log.result(bot_id = x, date = str(d.today()), start_time = start_time, finish_time = time(), time_list = time_list, revenue_list = earnings_list)

    log.result(bot_id = x, date = str(d.today()), start_time = start_time, finish_time = time(), time_list = time_list, revenue_list = earnings_list)
    listening_messages(x, cur, opts, client)


def balance(client):
    client.send_message('LTC Click Bot', '💰 Balance')
    sleep(0.7)
    dp = client.get_entity('LTC Click Bot')
    messages = client.get_messages(dp, limit=1)

    for message in messages:
        
        text = message.message.split(':')[1].split('LTC')[0]

    balance = text.split()
    balance = ''.join(balance)
    balance = float(balance)
    print(balance)
    
    return balance


def wating(x, opts, cur, client):

    sleep(3600)
    bot(x, opts, cur, client)


def start_client(x):
    db = sqlite3.connect('Accounts.db')
    cur = db.cursor()

    print("Очередь аккаунта № " + str(x))
    cur.execute(f"SELECT PHONE FROM telegram WHERE ID = '{x}'")
    sleep(0.2)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)
    cur.execute(f"SELECT PASSWORD FROM telegram WHERE ID = '{x}'")
    sleep(0.2)
    password = str(cur.fetchone()[0])
    print(password)
    cur.execute(f"SELECT API_ID FROM telegram WHERE ID = '{x}'")
    sleep(0.2)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM telegram WHERE ID = '{x}'")
    sleep(0.2)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))
    client = TelegramClient(session, api_id, api_hash)
    client.start()
    
    db.close()

    return client

def browser(driver, url, time = 0):
    
    try:
        driver.get(url)
        sleep(2)
        time = driver.find_element_by_class_name('timer').text.split('wait')[1].split(' ')[1]
        time = int(time) + 3
        print(time)

        sleep(time)

    except:
        time = 13
        sleep(time)

    num_of_tabs = 1

    for x in range(0, num_of_tabs):
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'W')

def checking_link_list(linkl_list):

    a = [item for item, count in collections.Counter(linkl_list).items() if count > 1]
    i = len(a)

    if i == 0:
        print('совпадений нет')

        return False

    if i>4:

        return True

def listening_messages(x, cur, opts, client):

    i = 0
    while True:
        
        time = random.randint(4,5)

        sleep(time)

        #client.send_message('LTC Click Bot', '🖥 Visit sites')
        
        dp = client.get_entity('LTC Click Bot')
        messages = client.get_messages(dp, limit=1)
        for message1 in messages:
            text = message1.message.split('😟')[0]
        print(text)
        
        if text == 'Sorry, there are no new ads available. ':
            print('заданий нет')

        if text == 'There is a new site for you to /visit! 🖥':
            print('Есть новое задание')
            bot(x, opts, cur, client)
        i = i+1

        if i >= 3 :

            bot(x, opts, cur, client)
            


def method_2(x, opts, cur, client):
    while True:

        client.send_message('LTC Click Bot', '🖥 Visit sites')
        sleep(2)

        dp = client.get_entity('LTC Click Bot')
        messages = client.get_messages(dp, limit=1)

        for message in messages:
        
            text = message.message

        try:
            url = text.split('---------------------')[1].split('❤❤❤❤❤❤❤❤❤')[1].split('\n')
            #a = len(url)
            #url = url.split('\n')
            print(url)

        except:
            url = text.split('---------------------')[1]
            #a = len(url)
            #url = url.split('\n')
            print(url)

def bot(x, opts, cur, client):
    d = datetime.date(2020,1,20)
    log.create_log(bot_id = x, date = d.today())
    start_time = time()
    earnings_list = []
    time_list = []
    cycles_passed = 0
    driver = Firefox(options=opts)
    link_list = []
    i = 0
    try:
        while True:

            startTime = time()
            start_balance = balance(client)

            try:
                time1 = random.randint(1, 2)
                sleep(time1)
                client.send_message('LTC Click Bot', '🖥 Visit sites')
                sleep(1.5)

                dp = client.get_entity('LTC Click Bot')
                messages = client.get_messages(dp, limit=1)
            
                for message in messages:
                    a = message.reply_markup
                    url = a.rows[0].buttons[0].url
                print(url)
                link_list.append(url)
                
                browser(driver,url)
                
                end_balance = balance(client)
                total_balance = end_balance - start_balance
                total_balance = total_balance * 11590
                earnings_list.append(total_balance)


                endTime = time() #время конца замера
                totalTime = endTime - startTime #вычисляем затраченное время
                print(totalTime)
                time_list.append(totalTime)

                log.cycle_log(bot_id = x, link = url, time_work = totalTime, revenue = total_balance, cycle_number = cycles_passed)

            except:
                driver.quit()
                no_task(x, cur, opts, client, driver, time_list, earnings_list, cycles_passed, start_time)
                #bot(x, opts, cur, client)

                
               
        
            if cycles_passed >= 5:
                
                checking_link_list = checking_link_list(link_list)
                link_list = []

                if checking_link_list == True :
                    
                    no_task(x, cur, opts, client, driver, time_list, earnings_list, cycles_passed, start_time)

                    break
            
            cycles_passed = cycles_passed + 1
            print('Цикл пройден за: ' + str(totalTime) + ' Циклов пройдено: '+ str(cycles_passed) + ' Заработанно: '+ str(total_balance))

    except:

        pass
            
            

def main(x):


    db = sqlite3.connect('Accounts.db')
    cur = db.cursor()
    opts = Options()
    opts.set_headless()
    assert opts.headless

    client = start_client(x)
    #balance(client)
    bot(x, opts, cur, client)
    #method_2(x, opts, cur, client)

    

if __name__ == "__main__":

    #x = sys.argv
    #x = int(x[1])
    x = 1
    print(x)
    main(x)