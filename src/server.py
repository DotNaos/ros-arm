import asyncio
import websockets
from pyngrok import ngrok

async def start_server(ip="0.0.0.0", port=8765):
        start_server = websockets.serve(echo, ip, port)
        print(f"Server started at ws://{ip}:{port}")
        public_url = ngrok.connect(port, "http", hostname="summary-amazing-tetra.ngrok-free.app")
        print(public_url)
        await start_server

async def echo():
    pass

async def main():
    await start_server
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
