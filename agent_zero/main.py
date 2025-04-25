import os
from fastapi import WebSocket
from browser_use import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from agent_zero.controller import get_controller
from agent_zero.tasks import tasks
from agent_zero.tasks_manager import AgentFactory, TaskManager

load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")
sensitive_data = {'fgg_user_name': os.getenv("FGG_USER_ID"), 'fgg_password': os.getenv("FGG_PASSWORD")}

browser = Browser(
    config=BrowserConfig(
        headless=False,
        disable_security=False,
        keep_alive=True,
        new_context_config=BrowserContextConfig(
            keep_alive=True,
            disable_security=False,
        ),
        # browser_binary_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )
)


async def start_agent_zero(socket: WebSocket = None, queue: asyncio.Queue = None):
    print('Starting agent_zero')
    async with await browser.new_context() as context:
        controller = get_controller(socket, queue)

        factory = AgentFactory(
            llm=llm,
            sensitive_data=sensitive_data,
            browser=browser,
            browser_context=context,
            save_path="logs/conversation",
            controller=controller,
        )

        manager = TaskManager(factory)

        # run everything:
        await manager.execute_all(tasks)

    await browser.close()

    input('Press Enter to close the browser...')


if __name__ == "__main__":
    asyncio.run(start_agent_zero())
