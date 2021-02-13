import json, math, re
from datetime import date, timedelta
import datetime

def exch_article(tit, chul_ma):

    ###해체분류구간####
    tit = tit.replace(',','')  #쉼표 뗌
    if bool(re.search('내린|오른', tit)):  #내린/오른을 경계로 앞뒤로 나눔. '내린''오른'이 없으면 오류 처리.
        front = re.sub(r'[내린|오른].+','',tit)
        back = re.sub(r'.+[내린|오른]','',tit)
        point = re.findall(r'\d+\.?\d*?원',front)[0].replace('원','')
        num = re.findall(r'\d+\.?\d*?원', back)[0].replace('원','')
        plma_ment = re.findall('내린|오른',tit)[0]
        if plma_ment == '오른':
            plma = True
        elif plma_ment == '내린':
            plma = False
    else:
        raise('연합 환율 제목에 "내린", "오른"  없음.')
    jisu_dict_s = {}
    jisu_dict_s['원/달러'] = {'name': '원/달러', 'num': num, 'plma': plma, 'plma_ment': plma_ment, 'point': point, 'rate': '0'}


    ###작성구간####
    if chul_ma == 'chul':
        st_en = '출발'
    elif chul_ma == 'ma':
        st_en = '마감'
    today = date.today().day
    name_h = '달러/원'  #한글이름
    name = '원/달러'
    point = jisu_dict_s[name]['point'] # 원
    point = str(float(point))
    num = jisu_dict_s[name]['num']
    num = str(float(num))
    plma_ment = jisu_dict_s[name]['plma_ment']
    title = f"""[{name_h}] 환율 {point}원 {plma_ment} {num}원 {st_en} """
    article = f"""{today}일 {name_h}"""

    #return값 설정
    result = {}
    result['send'] ={'title':title, 'article':article}
    result['data'] = jisu_dict_s['원/달러']
    return result

def ko_article(tit, chul_ma, ko):
    if ko == 'kospi':
        name_h = '코스피'  #한글이름
        name = 'KOSPI'
    elif ko == 'kosdaq':
        name_h = '코스닥'  #한글이름
        name = 'KOSDAQ'
    today = date.today().day

    if chul_ma == 'chul':
        st_en = '출발'
    elif chul_ma == 'ma':
        st_en = '마감'

    ####해체분류구간#####
    tit = tit.replace(',','')  #쉼표 뗌
    if bool(re.search('내린|오른', tit)):  #내린/오른을 경계로 앞뒤로 나눔. '내린''오른'이 없으면 오류 처리.
        front = re.sub(r'[내린|오른].+','',tit)
        back = re.sub(r'.+[내린|오른]','',tit)
        point = re.findall(r'\d+\.?\d*?(?=[pP])',front)[0].replace('원','')
        rate = re.findall(r'\d+\.?\d*?(?=%)',front)[0].replace('원','')
        num = re.findall(r'\d+\.?\d*', back)[0].replace('원','')
        # print(point)
        # print(rate)
        # print(num)
        plma_ment = re.findall('내린|오른',tit)[0]
        if plma_ment == '오른':
            plma = True
        elif plma_ment == '내린':
            plma = False
    else:
        raise(f'연합 {ko} 제목에 "내린", "오른"  없음.')
    jisu_dict_s = {}
    jisu_dict_s[f'{ko}'] = {'name': name, 'num': num, 'plma': plma, 'plma_ment': plma_ment, 'point': point,
                            'rate': rate}
    title = f"""[{name_h}] {point}p({rate}%) {plma_ment} {num} {st_en} """
    article = f"""{today}일 {name_h} {st_en}"""
    # print(title)
    # print(article)


    ##return값 설정
    result = {}
    result['send'] ={'title':title, 'article':article}
    result['data'] = jisu_dict_s[f'{ko}']
    return result

def second_bo(jisu_dict_s=None, chul_ma = None):

    today = date.today().day
    yesterday = (date.today() - timedelta(days=1)).day
    now_0 = str(datetime.datetime.now().hour) +'시' + str(datetime.datetime.now().minute) +'분'
    g = {} #글로벌
    ##
    n = {
        'kp':'kospi',
        'kd':'kosdaq',
        'ex':'원/달러'
    }
    for i in ['kp','kd','ex']:
        ind = n[i]
        temp = jisu_dict_s[ind]['point'] # 코스피 변동폭
        g[i+'_point'] = str(float(temp))
        temp = float(jisu_dict_s[ind]['num']) #코스피 얼마
        g[i+'_sun'] = math.floor(temp/10)*10
        g[i+'_num'] = str(temp)
        g[i+'_plma'] = jisu_dict_s[ind]['plma'] #증감여부

        g[i+'_plma_ment'] = jisu_dict_s[ind]['plma_ment']
        g[i+'_rate'] = float(jisu_dict_s[ind]['rate']) #변동폭
        #
        if g[i+'_rate'] < 0.5 :
            g[i+'_how'] = '소폭 '
            g[i+'_how2'] = ''
        elif g[i+'_rate'] <2:
            g[i+'_how'] = ''
            g[i+'_how2'] = ''
        elif g[i+'_rate'] >2:
            g[i+'_how'] = '대폭 '
            g[i+'_how2'] = '급격히 '
        #
        if g[i+'_plma']:
            g[i+'_ment_sang'] = '상승'
            g[i+'_ment_se'] = '오름세'
            g[i+'_ment_jin'] = '높아진'
            g[i+'_arr'] = '↑'
        elif not g[i+'_plma']:
            g[i+'_ment_sang'] = '하락'
            g[i+'_ment_se'] = '내림세'
            g[i+'_ment_jin'] = '떨어진'
            g[i+'_arr'] = '↓'

    ks_kd = '는' #코스피 코스닥 같으면 '도'
    if g['kp_plma'] == g['kd_plma']:
        ks_kd = '도'
    if chul_ma == 'chul': #출발

        title = f"""코스피, 장초반 {g['kp_how']}{g['kp_ment_sang']} {g['kp_sun']}선...코스닥 {g['kd_rate']}%{g['kd_arr']}(2보)"""
        article = f"""{today}일 장초반 코스피 지수는 {g['kp_how']}{g['kp_plma_ment']} {g['kp_sun']}선을 가리키고 있다. 코스닥{ks_kd} 
{g['kd_ment_se']}다. <br><br>이날 오전 {now_0} 기준 코스피는 전날 종가와 비교해 {g['kp_point']}포인트(p)({g['kp_rate']}%) {g['kp_plma_ment']}
{g['kp_num']}를 기록 중이다.<br><br>코스닥은 전날보다 {g['kd_point']}p({g['kd_rate']}%) {g['kd_ment_jin']} {g['kd_num']}를 가리키고 있다.<br><br>서울외환시장에서 달러/원 환율은 전날 대비 {g['ex_point']}원 {g['ex_plma_ment']} {g['ex_num']}원으로 거래를 시작했다."""
    elif chul_ma == 'ma': #마감
        title = f"""코스피 {g['kp_rate']}% {g['kp_how']}{g['kp_ment_sang']} {g['kp_sun']}선...코스닥 {g['kd_rate']}%{g['kd_arr']}(2보)"""
        article = f"""{today}일 코스피 지수가 {g['kd_rate']}% {g['kp_how']}{g['kp_ment_sang']}해 {g['kp_sun']}선으로 마감했다. 코스닥
{ks_kd} {g['kd_ment_se']}였다. <br><br>이날 코스피 지수는 {g['kp_point']}포인트(p)({g['kp_rate']}%) {g['kp_plma_ment']} 
{g['kp_num']}로 거래를 마쳤다.<br><br>코스닥 지수는 {g['kd_point']}p({g['kd_rate']}%) {g['kd_plma_ment']}{g['kd_num']}로 
마감했다.<br><br>달러/원 환율은 {g['ex_point']}원 {g['ex_plma_ment']} {g['ex_num']}원을 기록했다."""
    return {'title':title, 'article':article}

if __name__ == '__main__':
    print(exch_article('[외환] 원/달러 환율 2.5원 내린 1,100.7원(마감)', 'ma'))
    print(ko_article('[코스피] 33.08p(1.07%) 오른 3,120.63(장종료)','ma','kospi'))