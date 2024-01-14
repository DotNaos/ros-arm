import asyncio
import websockets
from pyngrok import ngrok
from visualizer import Visualizer

visualizer = Visualizer()

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)
        visualizer.update(message)

async def run_visualizer():
    while True:
        visualizer.run()
        await asyncio.sleep(0)  # Yield control to the event loop

async def main():
    start_server = websockets.serve(echo, "0.0.0.0", 8765)
    public_url = ngrok.connect(8765, "http", hostname="summary-amazing-tetra.ngrok-free.app")
    print(public_url)


    # Create the visualizer task
    visualizer_task = asyncio.create_task(run_visualizer())

    await start_server
    await visualizer_task

asyncio.run(main())
