import requests
import cv2
import numpy as np
import base64
import sys


def get_frame():
    
    url = 'http://172.17.129.74:5858/stream'
    
    while True:
        response = requests.get(url, stream=True)
    
        nparr = np.frombuffer(response.content, dtype=np.uint8)
        
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        print(frame)
        # cv2.imshow("frame", frame)
        
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     print("exit")


if __name__ == '__main__':
    get_frame()
