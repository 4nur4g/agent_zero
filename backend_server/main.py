import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from backend_server.handlers.websocket_handler import handle_socket

# Store active WebSocket connections

connections: Dict[WebSocket, dict] = {}
active_connections: Dict[str, WebSocket] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.connections = {} 
    app.state.active_connections = {}
    app.state.response_queues = {}

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# WebSocket endpoint to handle connections
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    queue = asyncio.Queue()
    # Accept the WebSocket connection
    await websocket.accept()
    await handle_socket(websocket, client_id, queue)


def start():
    """To run the development server"""
    uvicorn.run("backend_server.main:app", host="0.0.0.0", port=3006, reload=True)


if __name__ == "__main__":
    start()
