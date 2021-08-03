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


class DataBase():

    def __init__(self, con, bot_id):
        
        self.con = con
        self.cur = self.con.cursor()
        self.bot_id = bot_id

    def crete_session(self):
        
        print("Очередь аккаунта № " + str(self.bot_id))
        self.cur.execute(f"SELECT PHONE FROM telegram WHERE ID = '{self.bot_id}'")
        sleep(0.2)
        Phone = str(self.cur.fetchone()[0])
        print("Входим в аккаунт: " + Phone)
        self.cur.execute(f"SELECT PASSWORD FROM telegram WHERE ID = '{self.bot_id}'")
        sleep(0.2)
        password = str(self.cur.fetchone()[0])
        print(password)
        self.cur.execute(f"SELECT API_ID FROM telegram WHERE ID = '{self.bot_id}'")
        sleep(0.2)
        api_id = str(self.cur.fetchone()[0])
        self.cur.execute(f"SELECT API_HASH FROM telegram WHERE ID = '{self.bot_id}'")
        sleep(0.2)
        api_hash = str(self.cur.fetchone()[0])
        self.con.close()
        session = str("anon" + str(self.bot_id))
        client = TelegramClient(session, api_id, api_hash)
        client.start()

        return client



class Bot:

    def __init__(self, bot_id, client):

        self.client = client
        self.bot_id = bot_id

        self.time_list = []
        self.earnings_list = []
        self.start_time = time()
        self.i = 0

        opts = Options()
        opts.set_headless()
        assert opts.headless

        self.driver = Firefox(options = opts)

        log.create_log(bot_id = bot_id, date = str(datetime.datetime.now()))


    def browser(self):
        
        try:
            self.driver.get(self.url)
            sleep(6.70)
            time =self.driver.find_element_by_class_name('timer').text.split('wait')[1].split(' ')[1]
            time = int(time) + 0.5
            print(time)
            sleep(time)

        except:
            time = 10
            sleep(time)

        num_of_tabs = 1

        for x in range(0, num_of_tabs):
            self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'W')

            

    def listening_messages(self):
        i = 0
        while True:
            i = i+1
            sleep(random.randint(0, 15))
            #client.send_message('LTC Click Bot', '🖥 Visit sites')

            dp = self.client.get_entity('LTC Click Bot')
            messages = self.client.get_messages(dp, limit=1)
            for message1 in messages:
                text = message1.message
        
            if text == 'There is a new site for you to /visit! 🖥':
                print('Есть новое задание')
                self.i =0
                self.start_time = time()

                log.create_log(bot_id = self.bot_id, date = str(datetime.datetime.now()))
                sleep(2)

                Bot.main_cycle(self)

            if i >=10:
                i = 0
                break
        Bot.main_cycle(self)
            
    def no_task(self):
        print('No task')
        log.result(bot_id = self.bot_id, date = str(datetime.datetime.now()), start_time = self.start_time, finish_time = time(), time_list = self.time_list, revenue_list = self.earnings_list, cycles = self.cycles_number)
        self.time_list = []
        self.earnings_list = []
        self.cycle_number = 1
        self.i = 0
        Bot.listening_messages(self)



    def balance(self):
        sleep(0.5)
        client = self.client

        client.send_message('LTC Click Bot', '💰 Balance')
        dp = client.get_entity('LTC Click Bot')
        sleep(0.25)
        messages = client.get_messages(dp, limit=1)

        for message in messages:

            text = message.message.split(':')[1].split('LTC')[0]

        balance = text.split()
        balance = ''.join(balance)
        balance = float(balance)
    
        return balance



    def main_cycle(self):
        cycles_number = 1
        self.cycles_number = cycles_number
        bot_id = self.bot_id
        a = True

        while a == True:

            startTime = time()
            start_balance = Bot.balance(self)

            try:
               
                sleep(0.75)
                self.client.send_message('LTC Click Bot', '🖥 Visit sites')
                sleep(0.5)

                dp = self.client.get_entity('LTC Click Bot')
                messages = self.client.get_messages(dp, limit=1)
            
                for message in messages:

                    text = message.message.split('😟')[0]
                    
                    if text == 'Sorry, there are no new ads available. ':
                        
                        while True:
                            self.client.send_message('LTC Click Bot', '🖥 Visit sites')
                            sleep(2)

                            dp = self.client.get_entity('LTC Click Bot')
                            messages = self.client.get_messages(dp, limit=1)

                            for message in messages:

                                text = message.message.split('😟')[0]
                            
                                if text == 'Sorry, there are no new ads available. ':
                                    self.i = self.i + 1
                                    print(self.i)

                                    if self.i >= 3:

                                        Bot.no_task(self)
                                        break

                                else:

                                    break

                    url = message.reply_markup.rows[0].buttons[0].url
                    self.url = url


                Bot.browser(self)
                sleep(0.3)
                end_balance = Bot.balance(self)
                total_balance = end_balance - start_balance
                total_balance = total_balance * 10400
                self.earnings_list.append(total_balance)

                endTime = time() #время конца замера
                totalTime = endTime - startTime #вычисляем затраченное время
        
                self.time_list.append(totalTime)
                sleep(0.5)

                file = open("logs" + '\Bot'+str(bot_id)+'.txt', 'a')

                file.write('\n\n' + str(cycles_number) + '.Link:' + str(url) + '\n Date:' + str(datetime.datetime.now()) + '\n  Time work:' + str(totalTime) + '\n' + '  Revenue RUB:' + str(total_balance))

                file.close()
                print(self.url)

                cycles_number = cycles_number + 1
            
                self.cycles_number = cycles_number

                if cycles_number <=10:
                    a = False
                    log.result(bot_id = self.bot_id, date = str(datetime.datetime.now()), start_time = self.start_time, finish_time = time(), time_list = self.time_list, revenue_list = self.earnings_list, cycles = self.cycles_number)
                    break

            except:
                pass

            self.bot_id = self.bot_id + 1
            self.driver.quit()
            main(bot_id = self.bot_id)



def main(bot_id):

    if bot_id >=5:
        bot_id = 0
    
    con = sqlite3.connect('Accounts.db')

    db = DataBase(con, bot_id)
    client = DataBase.crete_session(db)
    bot = Bot(bot_id = bot_id, client = client)

    Bot.main_cycle(bot)

if __name__ == "__main__":
    main(1)