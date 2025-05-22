import asyncio
import websockets
import http.server
import socketserver
import threading

connected = set()

# WebSocket handler
async def handler(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    finally:
        connected.remove(websocket)

# HTTP server for frontend
def start_http():
    PORT = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"📡 HTTP Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Async main for WebSocket
async def main():
    print("🔌 WebSocket Server running at ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    threading.Thread(target=start_http, daemon=True).start()
    asyncio.run(main())
