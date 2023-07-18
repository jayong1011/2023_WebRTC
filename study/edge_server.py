from flask import Flask, request, Response
import cv2
import numpy as np
from config import * 

app = Flask(__name__)

roi_coordinates = (100, 100, 800, 800)

data = {}
def frame():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read(0)
        # frame = cv2.resize(frame,(1024,480))
        
        # 검은 화면 출력
        # black_screen = np.zeros(frame.shape, dtype=np.uint8)
        
        start_x, start_y, end_x, end_y = roi_coordinates
        roi = frame[start_y:end_y, start_x:end_x]
        
        _, buffer = cv2.imencode('.jpg', roi ,[int(cv2.IMWRITE_JPEG_QUALITY), 60])
        frame  = buffer.tobytes()
    
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 반환
        
         



 # 서버 정상적으로 실행되었는지 확인
@app.route('/')
def main():
        return Response(frame(), mimetype ='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(HOST, port=8000, debug=True)