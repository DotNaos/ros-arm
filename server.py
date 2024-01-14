import asyncio
import websockets
from pyngrok import ngrok
from visualizer import Visualizer
from motor import Motor_control


class Server:
    def __init__(self, ip="0.0.0.0", port=8765, visualize=False):
        self.ip = ip
        self.port = port
        self.visualize = visualize
        self.motor_control = Motor_control()

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.run())
        asyncio.get_event_loop().run_forever()

    async def run(self):
        self.start_server = websockets.serve(self.echo, self.ip, self.port)
        print(f"Server started at ws://{self.ip}:{self.port}")
        self.public_url = ngrok.connect(self.port, "http", hostname="summary-amazing-tetra.ngrok-free.app")
        print(self.public_url)
        await self.start_server

        if self.visualize:
            print("Starting Visualizer")
            self.visualizer = Visualizer()
            # Create the visualizer task
            self.visualizer_task = asyncio.create_task(self.run_visualizer())
            await self.visualizer_task


    async def echo(self, websocket, path):
        async for message in websocket:
            # await websocket.send(message)
            self.motor_control.update(message)
            if self.visualize:
                self.visualizer.update(message)

    async def run_visualizer(self):
        while True:
            self.visualizer.run()
            await asyncio.sleep(0)  # Yield control to the event loop
