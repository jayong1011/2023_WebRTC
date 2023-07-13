from flask import Flask, request, Response
import cv2
from config import * 

app = Flask(__name__)

data = {}
 
 # 서버 정상적으로 실행되었는지 확인
@app.route('/')
def main():
    
    print("ddddd")

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read(0)
        print(frame)
    
        #해상도 줄여서 데이터 크기 축소(화질떨어짐)
        frame = cv2.resize(frame,(640, 480))
        _, buffer = cv2.imencode('.jpg', frame,[int(cv2.IMWRITE_JPEG_QUALITY), 60])


        return buffer


if __name__ == '__main__':
    app.run(HOST, port=8000, debug=True)