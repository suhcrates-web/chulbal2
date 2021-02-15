from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import os, glob, json, requests
import time, re, post
from article import exch_article, ko_article, second_bo
from telebot import bot


url = 'https://www.yna.co.kr/news/1'  # 전체 '최신기사'에 먼저 뜨고 '경제 전체기사'에는 좀 나중에 듬.
# url ='https://www.yna.co.kr/economy/all/1'
req = requests.get(url)
be_0 = BeautifulSoup(req.text, 'html.parser')
li_list = be_0.find('div', {'class':'section01'}).find_all('li')

if li_list == []: #이러면 뭔가 잘못된거임.
    raise Exception("연합 클래스 바뀜")

#1면 제목리스트 만들어짐
tit_list = []
li_er_n=0
for i in li_list:
    try:
        i = i.strong.text
        tit_list.append(i)
    except:
        pass


print(tit_list)