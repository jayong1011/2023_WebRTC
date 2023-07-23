from flask import Flask, request, Response
import cv2
import numpy as np
import keyboard
from config import * 

app = Flask(__name__)

roi_coordinates = [0, 0, 800, 800]

data = {}

fixel = []

def fixel_control(part):
    if keyboard.is_pressed(80):
        part[0] = part[0]-100
        part[1] = part[1]-100
        
    elif keyboard.is_pressed(70):
        part[0] = part[0]+100
        part[1] = part[1]+100
    
    else:
        
        return part
    
def frame():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read(0)

        
        if ret:
            output_frame = np.zeros_like(frame, dtype=np.uint8)
        
            fixel = fixel_control(roi_coordinates)
            
            start_x, start_y, end_x, end_y = fixel[0], fixel[1], fixel[2], fixel[3]
            
            roi = frame[start_y:end_y, start_x:end_x]
            
            output_frame[start_y:end_y, start_x:end_x] = roi
            
            # cv2.rectangle(output_frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)  # 녹색 와이어프레임
            
        
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