from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

# foodlist DB에 저장
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
# db = client.dbsparta_plus_week3

client = MongoClient('localhost', 27017)
db = client.foodlist

driver = webdriver.Chrome('./chromedriver')

# 생생정보통 맛집 스크래핑
url = "https://menutong.com/bbs/board.php?bo_table=sangto"

driver.get(url)
time.sleep(5)

# 더 많은 페이지 크롤링
for i in range(4, 13):

    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')

    # 각 식당에 해당하는 카드 선택
    places = soup.select("#list-body > div")
    print(len(places))

    # 식당 이미지 src, href, 이름, 카테고리, 번호, 주소 가져오기
    for place in places:
        img = place.find('img')
        img_src = img['src']
        a = place.find('a')
        a_href = a['href']
        title = place.select_one(
            "div.list-text > div.list-text > div.text-muted.font-12 > font:nth-child(2) > b").text
        category = place.select_one(
            "div.list-text > div.list-text > div.text-muted.font-12 > font:nth-child(5) > b").text
        tel = place.select_one(
            "div.list-text > div.list-text > div.text-muted.font-12 > span:nth-child(7)").text
        address = place.select_one(
            "div.list-text > div.list-text > div.text-muted.font-12 > span:nth-child(9)").text

        # 문자열 인덱싱
        address = address[5:]

        # Geocoding 연결
        headers = {
            "X-NCP-APIGW-API-KEY-ID": "",
            "X-NCP-APIGW-API-KEY": ""
        }
        r = requests.get(
            f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
        response = r.json()

        # 주소에 오류 없는 경우만 출력
        if response["status"] == "OK":
            if len(response["addresses"]) > 0:
                x = float(response["addresses"][0]["x"])
                y = float(response["addresses"][0]["y"])
                print(title, address, category, img_src, x, y)
                # foodlist DB에 저장
                doc = {
                    "title": title,
                    "address": address,
                    "category": category,
                    "img_src": img_src,
                    "a_href": a_href,
                    "tel": tel,
                    "mapx": x,
                    "mapy": y}
                db.foodlist.insert_one(doc)
            else:
                print(title, address, "좌표를 찾지 못했습니다")
                print(address)
    btn_more = driver.find_element_by_css_selector(
        "#fboardlist > div.list-page.text-center > ul > li:nth-child(%d) > a" % (i))
    btn_more.click()
    time.sleep(5)
driver.quit()
