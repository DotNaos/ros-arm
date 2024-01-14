import asyncio
import websockets
from pyngrok import ngrok



async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

        print(message)

start_server = websockets.serve(echo, "127.0.0.1", 8765)
public_url = ngrok.connect(8765, "http", hostname="summary-amazing-tetra.ngrok-free.app")
print(public_url)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
