import asyncio
import json
import threading
import websockets
from pyngrok import ngrok
from control import Control

class Server:
    def __init__(self):
        self.control = Control()
        self.control_thread = threading.Thread(target=self.control.loop, daemon=True)
        self.control_thread.start()

        asyncio.get_event_loop().run_until_complete(self.run())
        asyncio.get_event_loop().run_forever()


    async def run(self, ip="0.0.0.0", port=8765):
        start_server = websockets.serve(self.echo, ip, port)
        print(f"Server started at ws://{ip}:{port}")
        public_url = ngrok.connect(port, "http", hostname="summary-amazing-tetra.ngrok-free.app")
        print(public_url)
        await start_server




    async def echo(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)

            # print(message)


            # Empty data
            if not data["landmarks"]:
                # print ("No data")
                continue

            if len(data["handednesses"]) == 2: # If there are two hands
                continue


            hand = "Right" # Default to right hand (IMPORTANT: First letter must be capital)

            # Only right hand
            if data["handednesses"][0][0]["categoryName"] == hand:
                self.control.update(data["landmarks"])
                # print(data)





# Reference for a message
# No Data:
# {"landmarks":[],"worldLandmarks":[],"handednesses":[],"handedness":[]}


#   "landmarks": [
#       [...], [...]
#   ],
#   "worldLandmarks": [
#       [...], [...]
#   ],
#
#   "handednesses": [
#     [
#       {
#         "score": 0.959747314453125,
#         "index": 1,
#         "categoryName": "Left",
#         "displayName": "Left"
#       }
#     ],
#     [
#       {
#         "score": 0.99462890625,
#         "index": 0,
#         "categoryName": "Right",
#         "displayName": "Right"
#       }
#     ]
#   ],
#   "handedness": [
#     [
#       {
#         "score": 0.959747314453125,
#         "index": 1,
#         "categoryName": "Left",
#         "displayName": "Left"
#       }
#     ],
#     [
#       {
#         "score": 0.99462890625,
#         "index": 0,
#         "categoryName": "Right",
#         "displayName": "Right"
#       }
#     ]
#   ]
# }

