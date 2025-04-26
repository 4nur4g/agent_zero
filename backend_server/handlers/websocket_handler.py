from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
from backend_server.langgraph.ai import chat

async def handle_socket(websocket: WebSocket, client_id: str, queue: asyncio.Queue):
    connections = websocket.app.state.connections
    connections[websocket] = {"client_id": client_id}
    active_connections = websocket.app.state.active_connections
    active_connections[client_id] = websocket
    websocket.app.state.response_queues[client_id] = queue

    print(f"Client {client_id} connected.")

    # TODO: Evoke it conditionally, i.e. when agent_zero is required

    try:
        while True:
            # Wait for a message from the client
            body = await websocket.receive_text()
            data = json.loads(body)
            text = data['requestBody']['message']
            msg_type = data['requestBody']['type']

            if(msg_type == 'to_agent_zero'):
                asyncio.create_task(websocket.app.state.response_queues[client_id].put(text))
            else:
                event_generator = await chat(websocket, text, client_id)
                # Iterating through the event_generator and sending each chunk over WebSocket
                async for chunk in event_generator:
                    await websocket.send_text(chunk)
                    await asyncio.sleep(0.05)  # simulate delay for streaming

            # TODO: To send response of user to agent_zero
    
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected.")
        del active_connections[client_id]  # Remove the WebSocket connection from the active connections
        del connections[websocket]