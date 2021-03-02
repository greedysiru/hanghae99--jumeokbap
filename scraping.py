from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests


client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus_week3

driver = webdriver.Chrome('./chromedriver')

# 생생정보통 맛집 스크래핑
url = "https://menutong.com/bbs/board.php?bo_table=sangto"

driver.get(url)
time.sleep(5)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')
# 각 식당에 해당하는 카드 선택
places = soup.select("list-body > div:nth-child(2) > div > div")
print(len(places))

# 식당 이름, 주소, 카테고리 가져오기
for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one(
        "div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one(
        "div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    print(title, address, category)
