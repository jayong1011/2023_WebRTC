from flask import Flask, request, Response, render_template
import json
from config import * 

app = Flask(__name__)

data = {}

@app.route('/')
def ok():
    return Response('{"status":"ok"}', status=200, mimetype='application/json')

@app.route('/class', methods=['POST','GET'])
def test():
    name = "김자용"
    carrer = "컴퓨터공학과"
    student_id = "20231612"
    year = 2023
    a ,b = 65 ,5
    return render_template('sample.html',a = a, name=name, b=b, student_id = student_id, carrer = carrer, year = year)


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
    if "offer" in data:
        j = json.dumps(data["offer"])
        del data["offer"]
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
    app.run(HOST, port=8080, debug=True)