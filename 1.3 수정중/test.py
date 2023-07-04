# _*_ coding: utf-8 _*_
import requests
import datetime
import time
import json

period = 5
test = True
# test = False

# 점심과 저녁 메뉴 업로드 시간을 확인하는 함수
def upload_time():
    count_menu = 0
    meal_fun([0, 1], 0)
    while True:
        current_time = time.perf_counter()
        
        # 17시 이후에는 저녁 메뉴 출력
        if int(datetime.datetime.now().strftime('%H')) == 17:
            while True:
                result = meal_fun([0, 1, 4], count_menu)
                if result:
                    print('저녁이 출력되었습니다.')
                    exit()
        
        # 11시 이후에는 점심 메뉴 출력
        elif count_menu == 0:
            while int(datetime.datetime.now().strftime('%H')) <= 11:
                result = meal_fun([0, 1], count_menu)
                if result:
                    print('점심이 출력되었습니다.')
                    count_menu += 1
                    break

        else:
            print(f'{period}초 후에 재탐색합니다.')
            sleep_time = period - time.perf_counter() + current_time
            if sleep_time > 0:
                time.sleep(sleep_time)

# 웹 사이트에서 식단 정보를 가져오는 함수
def access_key(num):
    # 오늘 날짜를 가져옴
    now = datetime.datetime.today().strftime("%Y%m%d")
    # 쿠키 정보
    cookies = {'remember-me': 'Y2pzcmhkODgyOjI2MjA1NDA3OTM2NTY6NzIwM2RkMzY1YzNhMWQ4MGE4NzRhOTNkYjJiN2FkOTY'}
    # 파라미터 설정 (날짜, 식사 종류, 레스토랑 코드)
    params = {'menuDt': now, 'menuMealType': num, 'restaurantCode': 'REST000213'}
    # 요청 보내기
    response = requests.get('https://welplus.welstory.com/api/meal', params=params, cookies=cookies)
    # JSON 형식으로 응답 받기
    menulist = json.loads(response.text)
    print(menulist)
    return menulist

# 점심과 저녁 메뉴를 파싱하고 출력할지 여부를 결정하는 함수
def meal_fun(num, count_menu):
    # 기본값은 11시 정각 사진이 있을시
    meal = 2
    picture = True
    # 현재 시간이 17시 이후인 경우 점심 메뉴 출력 
    if count_menu:
        meal = 3
        if int(datetime.datetime.now().strftime('%M')) >= 10:
            picture = False

     # 식단 정보를 순회하며 메뉴 출력 여부 결정
    for i in num:
        meal_dict = access_key(meal).get('data').get('mealList')[i]
        title = meal_dict.get("menuMealTypeTxt")  # 식사 종류(점심/저녁)
        menuname = meal_dict.get('subMenuTxt')  # 메뉴 이름
        kcal = meal_dict.get('kcal')  # 칼로리 정보
        course = meal_dict.get('courseTxt')  # 코스 정보

        # 사진이 있는 경우
        if picture:
            try:
                photo_url = meal_dict.get('photoUrl') + meal_dict.get('photoCd')  # 사진 URL
                menu_print(title, menuname, kcal, photo_url, course, test)  # 메뉴 출력 함수 호출 (사진 포함)
            except:
                print(f'{title} 사진이 없습니다. 5초뒤 재탐색 합니다.')
                time.sleep(period)
                return False
        # 사진이 없는 경우
        elif not picture:
            if meal == 3:
                photo_url_default = 'https://i.ytimg.com/vi/ritv9l9lJWs/mqdefault.jpg'
                menu_print(title, menuname, kcal, photo_url_default, course, test)  # 메뉴 출력 함수 호출 (사진 미포함)

    return True

# 메뉴 정보를 출력하는 함수
def menu_print(title, menuname, kcal, photo_url, course, test):
    
    field1 = '{"attachments": [{"fallback": "메뉴 업데이트","color": "#A1C0DE","title": "'
    field11 = '메뉴","title_link": "'
    field2 = '","fields": [{"short":false,"title":"오늘의 '
    field3 = '메뉴","value":"'
    field4 = '"},{"short":true,"title":"칼로리","value":"'
    field5 = '칼로리"},{"short":true,"title":"사진안보이면","value":"[이거 눌러]('
    field6 = ')"}],"image_url": "'
    field7 = '"}]}'
    values = field1 + title + course + field11 + photo_url + field2 + title + field3 + menuname + field4 + kcal + field5 + photo_url + field6 + photo_url + field7
    
    # 테스트 중일시
    if test:
        url = 'https://meeting.ssafy.com/hooks/e6qs4hmou7nxpm5e1x66xddjnh' # 서지호 - 연구소
        response = requests.post(url, data=values.encode('utf-8'))
    # 정상 서비스 중일시
    else:
        url_1 = 'https://meeting.ssafy.com/hooks/jmikd999yigfzxj53i7y7xtz3e' # 서지호 - 구미 3반
        url_2 = 'https://meeting.ssafy.com/hooks/nuu3ao3nb3dzixzmpm44m1pn7r' # 서지호 - 구미 전체 캠S
        response = requests.post(url_1, data=values.encode('utf-8'))
        response = requests.post(url_2, data=values.encode('utf-8'))


# 메인 함수 실행
if __name__ == "__main__":
    upload_time()

