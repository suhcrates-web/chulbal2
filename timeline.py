from datetime import datetime
from chul_ma import chul_ma, magam
# import article
# from make_dict import make_dict, magam_check, yon_data
# import post
import time
# from telebot import bot

def timeline():
    chulbal_done = False
    magam_done = False
    i=0
    while True:
        now= datetime.today().strftime(format='%H:%M')
        print('1/3')
        #출발
        if (now >= "09:00") and (now<="09:05"):
            while not chulbal_done:
                chul_ma('chul')
                chulbal_done = True
            time.sleep(600)
        print('2/3')
        #마감

        if (now >= "15:30") and (now<="15:50"):
            while not magam_done:
                chul_ma('ma')
                magam_done = True
            return print('출발마감봇 종료')

        print('here3')
        i= i+1
        time.sleep(1)
        print(str(now)+' '+str(i))

if __name__ == '__main__':
    timeline()