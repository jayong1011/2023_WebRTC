import requests
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
import asyncio
import base64
import cv2
import numpy as np
from config import *


ID = "answerer01"


async def main():
    
    print("Strating")
    peer_connection = RTCPeerConnection()
    
    
    @peer_connection.on("datachannel")
    def on_datachannel(channel):
        print(channel, "-", "created by remote party")
        channel.send("Hello From Answerer via RTC Datachannel")
        @channel.on("message")
        async def on_message(message):
      
      
            binary_data = base64.b64decode(message)

            buf = np.frombuffer(binary_data, np.uint8)

            image = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)

            #화면 출력
            cv2.imshow('image', image)
            cv2.waitKey(1)
           
        
    resp = requests.get(SIGNALING_SERVER_URL + "/get_offer")
    
    print(resp.status_code)
    if resp.status_code == 200:
        data = resp.json()
        if data["type"] == "offer":
            rd = RTCSessionDescription(sdp = data["sdp"], type=data["type"])
            await peer_connection.setRemoteDescription(rd)
            await peer_connection.setLocalDescription(await peer_connection.createAnswer())
            
            message = {"id": ID, "sdp" : peer_connection.localDescription.sdp, "type" : peer_connection.localDescription.type}
            r = requests.post(SIGNALING_SERVER_URL + '/answer' , data = message)
            # print(message)
            while True:
                # print("Ready for Stuff")
                await asyncio.sleep(1)


asyncio.run(main())