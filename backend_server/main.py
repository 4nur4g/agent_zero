import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


# Store active WebSocket connections
active_connections = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, Worgergrrld!"}

# WebSocket endpoint to handle connections
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # Accept the WebSocket connection
    await websocket.accept()
    
    # Add the WebSocket connection to the active connections dictionary
    active_connections[client_id] = websocket
    print(f"Client {client_id} connected.")
    
    try:
        while True:
            # Wait for a message from the client
            message = await websocket.receive_text()
            print(f"Message from {client_id}: {message}")
            
            # Send a response back to the client
            await websocket.send_text(f"{message}")
    
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected.")
        del active_connections[client_id]  # Remove the WebSocket connection from the active connections


def start():
    """To run the development server"""
    uvicorn.run("backend_server.main:app", host="0.0.0.0", port=3006, reload=True)


if __name__ == "__main__":
    start()
