from flask import Flask, request, Response
import json
from config import * 

app = Flask(__name__)

data = {}
 
 # 서버 정상적으로 실행되었는지 확인
@app.route('/')
def ok():
    return Response('{"status":"ok"}', status=200, mimetype='application/json')

# 전송하는 카메라 데이터 저장 
@app.route('/offer', methods=['POST'])
def offer():
    if request.form["type"] == "offer":
        data["offer"] = {"id" : request.form['id'], "type" : request.form['type'], "sdp":request.form['sdp']}
        return Response(status=200)
    
    else: 
        return Response(status=400)
    
@app.route('/answer', methods=['POST'])
def answer():
    if request.form["type"]  == "answer":
        data["answer"] = {"id" : request.form['id'], "type" : request.form['type'], "sdp":request.form['sdp']}
        return Response(status=200)
    else:
        return Response(status=400)
    

@app.route('/get_offer')
def get_offer():
    # 카메라 데이터 확인
    if "offer" in data:
        # 카메라 데이터 json객체로 저장
        j = json.dumps(data["offer"])
        # json객체로 저장한 데이터 삭제
        del data["offer"]
        # 상태 코드 및 json파일 반환
        return Response(j, status=200, mimetype='application/json')
    else: 
        return Response(status=503)
    
@app.route('/get_answer')
def get_answer():
    if "answer" in data:
        j = json.dumps(data["answer"])
        del data["answer"]
        return Response(j, status = 200, mimetype='application/json')
    else:
        return Response(status = 503)
    

if __name__ == '__main__':
    app.run(HOST, port=8000, debug=True)