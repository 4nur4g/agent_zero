from langgraph.graph.state import CompiledStateGraph
from backend_server.handlers.llm import get_llm, get_embedding_model
from backend_server.langgraph.rag import get_graph
from fastapi import WebSocket

collection_name = "knowledge_base_v10"
thread_id = str(45)

async def chat(websocket: WebSocket, msg):
    """
    Accepts a message in the request body and returns a response from the LLM.
    """
    print(f" data is coming here -->  {msg}")
    graph: CompiledStateGraph = await get_graph(get_llm(), get_embedding_model(), websocket.app.state.chroma_client,
                                                collection_name, websocket)
    print(f" i am coming back from graph {graph}")
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        async for message, metadata in graph.astream(
                {"messages": [{"role": "user", "content": msg}]},
                stream_mode="messages",
                config=config,
        ):
            if metadata["langgraph_node"] in ["query_or_respond", "generate"]:
                print(f" data is coming here -->  {metadata}")
                print(f" content of the message --> {message}")
                content = message.content
                yield f"data: {content}\n\n"

    return event_generator()
