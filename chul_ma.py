from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import os, glob, json, requests
import time, re, post
from article import exch_article, ko_article, second_bo
from telebot import bot

def chul_ma(chul_ma):
    kospi_did = False
    kosdaq_did = False
    exch_did = False
    second_bo_did = False

    kospi_up = False
    kosdaq_up = False
    exch_up = False

    jisu_dicts = {} # 2보 작성을 위한 정보
    #출발마감 여부
    if chul_ma == "chul":
        ko_word = '개장'
        ex_word = '개장'
        cm_num = '1'
        rm = '출발'
    elif chul_ma =="ma":
        ko_word = '장종료'
        ex_word = '마감'
        cm_num = '2'
        rm = '마감'
    today = datetime.today().strftime("%Y%m%d")
    n = 1


    while not (kospi_did and kosdaq_did and exch_did and second_bo_did):
        if n % 2 == 1:
            url = 'https://www.yna.co.kr/news/1'  # 전체 '최신기사'에 먼저 뜨고 '경제 전체기사'에는 좀 나중에 듬.
        else:
            url ='https://www.yna.co.kr/economy/all/1'
        n+=1

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
                # print(i)

                ##코스피, 코스닥, 외환 제제목 있는지 확인.
                if bool(re.search('\[코스피\]',i)) and bool(re.search('\('+ko_word+'\)',i)) :
                    print('연합 코스피 뜸')
                    kospi_up = True
                    kospi_tit = i
                if bool(re.search('\[코스닥\]',i)) and bool(re.search('\('+ko_word+'\)',i)) :
                    print('연합 코스닥 뜸')
                    kosdaq_up = True
                    kosdaq_tit = i
                if bool(re.search('\[외환\]',i)) and bool(re.search('\('+ex_word+'\)',i)) :
                    print('연합 환율 뜸')
                    exch_up = True
                    exch_tit= i

            except:
                li_er_n +=1
                pass #중간에 광고 껴있어서.
        # print(tit_list)
        print(f'li 중 에러 {li_er_n}개 있음')
        if not (kospi_up or kosdaq_up or exch_up):
            print('연합 아직 암것도 안뜸')
        else:
            print('뜬곳\n'+'코스피:'+str(kospi_up)+'\n'+'코스닥:'+str(kosdaq_up)+'\n'+'코스피:'+str(kosdaq_up)+'\n')


            #{'send': {'title': '[달러/원] 환율 2.5원 내린 1100.7원 마감 ', 'article': '13일 달러/원'}, 'data': {'원/달러': {'name': '원/달러', 'num': '1100.7', 'plma': False, 'plma_ment': '내린', 'point': '2.5', 'rate': '0'}}}
            #키값은 kospi kosdaq으로 소문자로.
        if kospi_up and not kospi_did:
            result = ko_article(kospi_tit, chul_ma, 'kospi')
            art = result['send']
            data = result['data']
            jisu_dicts['kospi'] =data
            kospi_did = True

            #post
            post.do_temp(title=art['title'], article=art['article'])
            post.do_mbot(title=art['title'], article=art['article'], rcept_no = str(today) + cm_num+ '1', rm=rm)
            bot('c' ,"코스피 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
            print('연합 코스피 -> 작성 완료')

        if kosdaq_up and not kosdaq_did:
            result = ko_article(kosdaq_tit, chul_ma, 'kosdaq')
            art = result['send']
            data = result['data']
            jisu_dicts['kosdaq'] =data
            kosdaq_did = True

            #post
            post.do_temp(title=art['title'], article=art['article'])
            post.do_mbot(title=art['title'], article=art['article'], rcept_no = str(today) + cm_num+ '2', rm=rm)
            print('연합 코스닥 -> 작성 완료')
        if exch_up and not exch_did:
            result = exch_article(exch_tit, chul_ma)
            art = result['send']
            data = result['data']
            jisu_dicts['원/달러'] =data
            exch_did = True  # 작성 완료

            #post
            post.do_temp(title=art['title'], article=art['article'])
            post.do_mbot(title=art['title'], article=art['article'], rcept_no = str(today) + cm_num+ '3', rm=rm)
            bot('c' ,"환율 올렸습니다\n"+"http://testbot.ddns.net:5231/bot_v3")
            print('연합 환율 -> 작성 완료')

        if (kospi_did and kosdaq_did and exch_did) and not second_bo_did:
            art = second_bo(jisu_dicts, chul_ma)
            second_bo_did = True

            #post
            post.do_temp(title=art['title'], article=art['article'])
            post.do_mbot(title=art['title'], article=art['article'], rcept_no = str(today) + cm_num+ '4', rm=rm)
            print('2보 작성 완료')

        time.sleep(5) #10초 간격으로 수행.
    print('시황 끝')
    time.sleep(600) #다 끝나면 10분 쉼



if __name__ == '__main__':
    chul_ma('ma')