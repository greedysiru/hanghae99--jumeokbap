from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
# db = client.dbsparta_plus_week3
# DB접근
client = MongoClient('localhost', 27017)
db = client.foodlist


# 결과페이지, 진자 변수 넘기기
@app.route('/resultpage')
def main():
    foodlist = list(db.foodlist.find({}, {"_id": False}))
    return render_template("result.html", foodlist = foodlist)

# 음식 리스트 반환 API
@app.route('/result', methods=["GET"])
def get_result():
    foods = list(db.foodlist.find({}, {"_id": False}))

    return jsonify({'result': 'success', 'foods': foods})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
