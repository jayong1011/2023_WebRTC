import requests
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
import asyncio
import base64
import cv2
import numpy as np
import socket
import json
from config import *


ID = "answerer01"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



async def main():
    
    print("Starting")
    peer_connection = RTCPeerConnection()
    

    @peer_connection.on("datachannel")
    def on_datachannel(channel):
        
        channel.send("Hello From Answerer via RTC Datachannel")
        
        @channel.on("message")
        async def on_message(message):
            
            binary_data = base64.b64decode(message)
                    
            buf = np.frombuffer(binary_data,  dtype=np.uint8)
            
            
            sock.sendto(buf, (SOCKET, PORT))
            
            
            # image = cv2.imdecode(buf, cv2.IMREAD_COLOR)

            # cv2.imshow('image', image)
            
            # cv2.waitKey(1)
            
            
        
    resp = requests.get(SIGNALING_SERVER_URL + "/get_offer")
    
    if resp.status_code == 200:
        data = resp.json()
        if data["type"] == "offer":
            rd = RTCSessionDescription(sdp = data["sdp"], type=data["type"])
            await peer_connection.setRemoteDescription(rd)
            await peer_connection.setLocalDescription(await peer_connection.createAnswer())
            
            message = {"id": ID, "sdp" : peer_connection.localDescription.sdp, "type" : peer_connection.localDescription.type}
            r = requests.post(SIGNALING_SERVER_URL + '/answer' , data = message)
   
            while True:
                await asyncio.sleep(1)


asyncio.run(main())