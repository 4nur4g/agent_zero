from langgraph.graph.state import CompiledStateGraph
from backend_server.handlers.llm import get_llm, get_embedding_model
from backend_server.langgraph.rag import get_graph
from fastapi import WebSocket
from datetime import datetime
import json

collection_name = "knowledge_base_v10"
thread_id = str(45)

async def chat(websocket: WebSocket, msg):
    """
    Accepts a message in the request body and returns a response from the LLM.
    """
    graph: CompiledStateGraph = await get_graph(get_llm(), get_embedding_model(), websocket.app.state.chroma_client,
                                                collection_name, websocket)
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        async for message, metadata in graph.astream(
                {"messages": [{"role": "user", "content": msg}]},
                stream_mode="messages",
                config=config,
        ):
            if metadata["langgraph_node"] in ["query_or_respond", "generate"]:
                # yield f"{message}\n\n"
                payload = {
                    "message": {
                        "text": message.content,
                        "image": '',
                    },
                    "additional_kwargs": getattr(message, "additional_kwargs", {}),
                    "response_metadata": getattr(message, "response_metadata", {}),
                    "id": getattr(message, "id", ""),
                    "type": getattr(message, "type", "from_ai"),
                    "timestamp": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                }
                yield f"data: {json.dumps(payload)}\n\n"

    return event_generator()

