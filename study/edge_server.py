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
def wireframe(frame,mask):
    
    cell_size = 200
    height, width = frame.shape[:2]
    
    
    grid_frame = frame.copy()
    grid_frame[mask != 255] = 0
    
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            # 원형 모양으로 자른 부분은 검은색으로 채우기
            if mask[y, x] == 0:
                cv2.rectangle(grid_frame, (x, y), (x + cell_size, y + cell_size), (0, 255, 0), 2)
                        

    return grid_frame

#원형 모양 
def shape_frame(frame, center_x,center_y):

    height, width = frame.shape[:2]
            
    center_x,center_y = shape_control(center_x, center_y)
    
    radius = min(center_x, center_y)
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 150, -1)
    
    # 원형 모양으로 자르기
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    return masked_frame,mask,center_x, center_y



# 원하는 부분 원형으로 출력
def shape():
    cap = cv2.VideoCapture(0)
    center_x, center_y = 1920 ,960
    
    while True:
        ret, frame = cap.read()  
        
        if ret:
            # 원형 모양 생성
            masked_frame , mask, center_x, center_y = shape_frame(frame,center_x,center_y)
        
            # 격자 모양 출력
            grid_frame = wireframe(frame,mask)
            
            #원형을 제외한 부분 격자 모양 출력
            result_frame = cv2.addWeighted(masked_frame, 1, grid_frame, 1, 0)


            _, buffer = cv2.imencode('.jpg', result_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                
    
            frame  = buffer.tobytes()
            
            # 웹 서버에서 영상 출력
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 반환



 # 웹서버 
@app.route('/')
def main():
        return Response(shape(), mimetype ='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(HOST, port=8000, debug=True)