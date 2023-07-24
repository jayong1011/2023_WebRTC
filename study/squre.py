from flask import Flask, request, Response
import cv2
import numpy as np
import keyboard
from config import * 


def fixel_control(part):
    if keyboard.is_pressed('down'):
        print("down")
        part[1] = part[1]+50
        part[3] = part[3]+50
        print(part[1],"-----------------",part[3])
        return part
    
    elif keyboard.is_pressed('up'):
        print("up")
        part[1] = part[1]-50
        part[3] = part[3]-50
        print(part[1],"-----------------",part[3])
        return part
    
    elif keyboard.is_pressed('left'):
        print("left")
        part[0] = part[0]-50
        part[2] = part[2]-50
        print(part[0],"-----------------",part[2])
        return part
    
    elif keyboard.is_pressed('right'):
        print("right")
        part[0] = part[0]+50
        part[2] = part[2]+50
        print(part[0],"-----------------",part[2])
        return part
    
    else:
        return part
    

def frame():
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print("Webcam Resolution: {}x{}".format(int(width), int(height)))

    while True:
        ret, frame = cap.read(0)

        if ret:
                        
            fixel = fixel_control(ROI)
            
            start_x, start_y, end_x, end_y = fixel[0], fixel[1], fixel[2], fixel[3]
            
            roi = frame[start_y:end_y, start_x:end_x]
            
        
            _, buffer = cv2.imencode('.jpg', roi ,[int(cv2.IMWRITE_JPEG_QUALITY), 60])
            
            frame  = buffer.tobytes()
    
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 반환
