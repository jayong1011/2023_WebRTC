from flask import Flask, request, Response
import cv2
import numpy as np
import keyboard
from config import * 

app = Flask(__name__)

# 픽셀 컨트롤 
def shape_control(center_x, center_y):
    
    if keyboard.is_pressed('left'):
            print("left")
            center_x -= 10
    elif keyboard.is_pressed('right'):
        print("right")
        center_x += 10
    elif keyboard.is_pressed('up'):
        center_y += 10
    elif keyboard.is_pressed('down'):
        center_y -= 10
        
    return center_x, center_y

#격자 그리기 
def wireframe(frame):
    cell_size = 200
    
    height, width = frame.shape[:2]
        
    grid_mask = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            cv2.rectangle(grid_mask, (x, y), (x + cell_size, y + cell_size), (0, 255, 0), 2)

    return grid_mask


# 원하는 부분 원형으로 출력
def shape():
    center_x, center_y = 1920 ,960
    cap = cv2.VideoCapture(0)
    
    cell_size = 200
    
    while True:
        ret, frame = cap.read()  
        
        if ret:
            # 원형 모양 생성
            height, width = frame.shape[:2]
            
            center_x,center_y = shape_control(center_x, center_y)
            
            radius = min(center_x, center_y)
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.circle(mask, (center_x, center_y), radius, 255, -1)
            
            # 원형 모양으로 자르기
            masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        
            
            _, buffer = cv2.imencode('.jpg', masked_frame ,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
            
            
            frame  = buffer.tobytes()
                    
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 반환
            
            # 원형 모양으로 영상 출력
            # cv2.imshow('Circular Webcam', masked_frame)


 # 서버 정상적으로 실행되었는지 확인
@app.route('/')
def main():
        return Response(shape(), mimetype ='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(HOST, port=8000, debug=True)