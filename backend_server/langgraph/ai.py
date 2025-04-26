from langgraph.graph.state import CompiledStateGraph
from backend_server.handlers.llm import get_llm, get_embedding_model
from backend_server.langgraph.rag import get_graph
from fastapi import WebSocket
import re
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
                # Extract all key=value pairs using regex
                pairs = re.findall(r"(\w+)=('[^']*'|\{[^}]*\}|\S+)", str(message))
                # Convert to dictionary (strip surrounding quotes)
                message_dict = {key: value.strip("'") for key, value in pairs}
                # Convert to JSON
                json_output = safe_parse_json(message_dict)
                yield f"{json_output}\n\n"

    return event_generator()

def safe_parse_json(value):
    if isinstance(value, str) and not value.strip():
        return ""  # handle empty string explicitly
    try:
        return json.dumps(value)
    except (json.JSONDecodeError, TypeError, ValueError):
        return value

