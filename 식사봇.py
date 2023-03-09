# _*_ coding: utf-8 _*_

import requests
import datetime
import time
import json

# --------------------------------------------------
period = 5  # 탐색 주기(초)
# --------------------------------------------------
lunch = 2 # access_key(2)
dinner = 3 # access_key(3)
def upload_time():
    count_time = time.perf_counter()
    count_menu = 0
    while True:
        count_time = time.perf_counter()
        if int(datetime.datetime.now().strftime('%H')) >= 17: # 17 시 넘었다면
        # if int(datetime.datetime.now().strftime('%H')) >= 11: 
        # if int(datetime.datetime.now().strftime('%M')) >= 37: # 분단위로 테스트용
            while True:
                result = meal_fun([0, 1, 4])
                if result == True:
                    print('저녁이 출력되었습니다.')
                    break
            break
        elif count_menu == 0:
            if int(datetime.datetime.now().strftime('%H')) >= 11: # 11 시 넘었다면
            # if int(datetime.datetime.now().strftime('%H')) >= 10: # 
                count_menu += 1
                while True:
                    result = meal_fun([0, 1])
                    if result == True:
                        print('점심이 출력되었습니다.')
                        break
                continue
            else:
                print(f'{period}초 후에 재탐색합니다.')
                if period > time.perf_counter() - count_time:
                    time.sleep(period - time.perf_counter() + count_time)
        else:
            print(f'{period}초 후에 재탐색합니다.')
            if period > time.perf_counter() - count_time:
                time.sleep(period - time.perf_counter() + count_time)

def access_key(num):
    now = datetime.datetime.today().strftime("%Y%m%d") # 오늘 날짜 코드
    # now = datetime.date(2023, 1, 27).strftime("%Y%m%d") # 지정 날짜 코드
    cookies = {
        'remember-me': ,
    }
    params = {
        'menuDt': now,
        'menuMealType': num,
        'restaurantCode': 'REST000213',
    }
    response = requests.get('https://welplus.welstory.com/api/meal', params=params, cookies=cookies)
    menulist = json.loads(response.text)
    
    # print(menulist)
    return menulist

def meal_fun(num):
    if int(datetime.datetime.now().strftime('%H')) >= 17: # 17 시 넘었다면
        meal = 3 # access_key
    elif int(datetime.datetime.now().strftime('%H')) >= 11: # 11 시 넘었다면
        meal = 2 # access_key

    for i in num:
        meal_dict = access_key(meal).get('data').get('mealList')[i]
        print(meal_dict)
        try:
            title = meal_dict.get("menuMealTypeTxt") # 점심, 저녁 정보
            menuname = meal_dict.get('subMenuTxt') # 메뉴목록 정보
            kcal = meal_dict.get('kcal') # 칼로리 정보
            photo_url = meal_dict.get('photoUrl') + meal_dict.get('photoCd') # 사진 정보
            course = meal_dict.get('courseTxt') # A코스 C코스 정보
            menu_print(title, menuname, kcal, photo_url, course)
        except:
            print(f'{title} 사진이 없습니다. 5초뒤 재탐색 합니다.')
            count_time = time.perf_counter()
            time.sleep(period - time.perf_counter() + count_time)
            return False
    return True

def menu_print(title, menuname, kcal, photo_url,course):
    # url = 'https://meeting.ssafy.com/hooks/e6qs4hmou7nxpm5e1x66xddjnh' # 서지호 - 연구소
    url_1 = 'https://meeting.ssafy.com/hooks/jmikd999yigfzxj53i7y7xtz3e' # 서지호 - 구미 3반
    url_2 = 'https://meeting.ssafy.com/hooks/nuu3ao3nb3dzixzmpm44m1pn7r' # 서지호 - 구미 전체 캠
    # now = datetime.date(2023, 1, 20).strftime("%Y%m%d") # 지정 날짜 코드
    # headers = {'Content-Type': 'application/json', }
    values = '{ "username": "Menu-Bot","text": "### ' + title + ' ' + course + '  :___nyamnyamgood_zoom:' + '\n' + menuname +' '+ kcal + ' kcal\n![음식사진]('+photo_url+')"}'
    # response = requests.post(url, data=values.encode('utf-8'))
    response = requests.post(url_1, data=values.encode('utf-8'))
    response = requests.post(url_2, data=values.encode('utf-8'))
#----------------------------------------------------------------------

if __name__ == "__main__":  
    upload_time()
