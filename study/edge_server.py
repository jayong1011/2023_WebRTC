import cv2
import numpy as np
import keyboard
import socket
import base64
from config import * 
from flask import Flask, request, Response, jsonify
import sys

app = Flask(__name__)

# 픽셀 컨트롤 
def shape_control(center_x, center_y):
    
    if keyboard.is_pressed('left'):
            print("left")
            center_x -= 30
    elif keyboard.is_pressed('right'):
        print("right")
        center_x += 30

    elif keyboard.is_pressed('up'):
        print("up")
        center_y += 17
    elif keyboard.is_pressed('down'):
        print("down")
        center_y -= 17
    elif keyboard.is_pressed('<'):
        print("zoom")
        center_x += 50
        center_y += 29
    elif keyboard.is_pressed('>'):
        print("reduction")
        center_x -= 50
        center_y -= 29
        
    return center_x, center_y

#격자 그리기 
def wireframe(frame,mask):

    grid_frame = np.zeros_like(frame)
    line_color = (0, 255, 0)
    line_thickness = 2


    for y in range(0, frame.shape[0], 100):
        cv2.line(grid_frame, (0, y), (frame.shape[1], y), line_color, line_thickness)

    for x in range(0, frame.shape[1], 100):
        cv2.line(grid_frame, (x, 0), (x, frame.shape[0]), line_color, line_thickness)

    # mask_outside_circle = cv2.bitwise_xor(mask)
    
    grid_frame = cv2.bitwise_and(grid_frame, grid_frame, mask=mask)
    
    
    return grid_frame

#원형 모양 
def shape_frame(frame, center_x,center_y):
    line_spacing = 150
    
    height, width = frame.shape[:2]
    
    center_x,center_y = shape_control(center_x, center_y)
    
    radius = min(center_x, center_y)
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 150, -1)
    
    # 원형 모양으로 자르기
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    
    for y in range(0, height, line_spacing):
        for x in range(0, width, line_spacing):
            if not mask[y, x]:
                cv2.line(masked_frame, (x, y), (min(x + line_spacing, width - 1), y), (255, 255, 255), 1)
                cv2.line(masked_frame, (x, y), (x, min(y + line_spacing, height - 1)), (255, 255, 255), 1)

    
    return masked_frame,center_x, center_y


def shape():
    
    cap = cv2.VideoCapture(0)
    
    center_x, center_y = 1280, 720
    
    desired_fps = 10
    
    cap.set(cv2.CAP_PROP_FPS, desired_fps)
    
    
    while True:
        
        ret, frame = cap.read()  
        
        if ret:
            # 원형 모양 생성
            frame = cv2.resize(frame,(2560,1440 ))
            
            masked_frame ,center_x, center_y = shape_frame(frame,center_x,center_y)
            
            #nparr = np.frombuffer(masked_frame, np.uint8)

            # numpy 배열을 이미지로 변환합니다.
            #frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


            _, buffer = cv2.imencode('.jpg', masked_frame)                        
            buffer = buffer.tobytes()
            
            
            cv2.imshow("frame", masked_frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
            
            #print(type(buffer)
            
            
            # yield (b'--frame\r\n'
            #           b'Content-Type: image/jpg\r\n\r\n' + buffer + b'\r\n')
            
            
            
 # 웹서버 
@app.route('/')
def main():
        return "hello World"
    
@app.route('/stream', methods = ['GET'])
def stream():

    return Response(shape(), mimetype = 'multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5858, debug=True)
