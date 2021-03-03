from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('localhost', 27017)
db = client.member
fooddb =client.foodlist


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.member.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('index.html', msg = msg)

# 결과페이지, 진자 변수 넘기기
@app.route('/resultpage')
def main():
    foodlist = list(fooddb.foodlist.find({}, {"_id": False}))
    return render_template("result.html", foodlist = foodlist)

# 음식 리스트 반환 API
@app.route('/result', methods=["GET"])
def get_result():
    foods = list(fooddb.foodlist.find({}, {"_id": False}))

    return jsonify({'result': 'success', 'foods': foods})

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    
    # pw를 암호화
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # id, 암호화된 pw 가지고 유저를 찾는다.
    result = db.member.find_one({'username': username_receive, 'password': pw_hash})
    # 찾은 경우
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        # 토큰 전달
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



# 회원정보 DB 저장
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    #회원 가입
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호

    }
    db.member.insert_one(doc)
    return jsonify({'result': 'success'})




#  ID 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.member.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
