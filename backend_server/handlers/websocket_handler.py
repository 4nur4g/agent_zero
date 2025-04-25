from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
from datetime import datetime

async def handle_socket(websocket: WebSocket, client_id: str): 
    connections = websocket.app.state.connections
    connections[websocket] = {"client_id": client_id}
    active_connections = websocket.app.state.active_connections
    active_connections[client_id] = websocket

    print(f"Client {client_id} connected.")
    
    try:
        while True:
            # Wait for a message from the client
            message = await websocket.receive_text()
            data = json.loads(message)
            text = data.get("message", "")
            print(f"Message from {client_id}: {text}")
            
            async for chunk in process_message(text):
                await websocket.send_text(chunk)
                await asyncio.sleep(0.05)  # simulate delay for streaming
    
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected.")
        del active_connections[client_id]  # Remove the WebSocket connection from the active connections
        del connections[websocket]


async def process_message(message: str):
    response = f"This is a streamed response to your message: {message}"
    for i in range(1, len(response) + 1):
        chunk = {
            "role": "agent",
            "content": response[i - 1],  # Send character-by-character
            "timestamp": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "isStreaming": True
        }
        yield json.dumps(chunk)
        await asyncio.sleep(0.01)  # Simulate delay

    # Final signal to indicate end of stream
    end_signal = {
        "role": "agent",
        "content": response,
        "timestamp": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        "isStreaming": False
    }
    print(f"end signal --> {end_signal} ")
    yield json.dumps(end_signal)