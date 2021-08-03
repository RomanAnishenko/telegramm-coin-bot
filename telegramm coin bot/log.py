import telethon
print(telethon.__version__)

def result(bot_id,date,start_time, finish_time, time_list, revenue_list, cycles):
    try:

        if len(time_list) >=0 and len(revenue_list) >=0:
            file = open("logs" + '\Bot'+str(bot_id)+'.txt', 'a')

            average_time = sum(time_list) / len(time_list)
            average_revenue_RUB = sum(revenue_list) / len(revenue_list)
            time_work = finish_time - start_time

            file.write('\n\nResult:' + '\n' + ' 1.Date:' + date + '\n 2.average time:' + str(average_time) + '\n 3.average revenue RUB:' + str(average_revenue_RUB) + '\n 4.Time work:' + str(time_work) + '\n Cycles:' + str(cycles)+'\n___________________________________________________________________________')
        else:
            file.write('\n\nResult:' +'\nСпски пусты')
    except:
        pass

def cycle_log(bot_id, link, time_work, revenue, cycle_number, date):
    print('1111111111111111')
    file = open("logs" + '\Bot'+str(bot_id)+'.txt', 'a')

    file.write('\n\n' + str(cycle_number) + '.Link:' + str(link) + '\n Date:' + str(date) + '\n  Time work:' + str(time_work) + '\n' + '  Revenue RUB:' + str(revenue))

    file.close()
def create_log(bot_id, date):


    bot_id = str(bot_id)
    file_name = "logs" + '\Bot'+ bot_id + '.txt'

    file = open(file_name, 'a')

    file.write('\nBot id: ' + bot_id + '\n' + 'Date: '+ str(date) + '\n')
    
    file.close()

