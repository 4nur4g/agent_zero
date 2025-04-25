import base64
import os

from browser_use.agent.views import ActionResult
from browser_use import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from browser_use.controller.service import Controller
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

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
    )
)

controller = Controller(exclude_actions=['search_google'])

@controller.action('Ask user for information')
async def ask_human(question: str, browser: BrowserContext) -> ActionResult:
    screenshot_b64 = await browser.take_screenshot()
    print(f"📷 Screenshot: {screenshot_b64}")
    os.makedirs("screenshots", exist_ok=True)
    with open("screenshots/my_capture.png", "wb") as f:
        f.write(base64.b64decode(screenshot_b64))
    answer = input(f'\n{question}\nInput: ')
    return ActionResult(extracted_content=answer)

async def main():
    async with await browser.new_context() as context:
        factory = AgentFactory(
            llm=llm,
            sensitive_data=sensitive_data,
            browser=browser,
            browser_context=context,
            save_path="logs/conversation",
            controller=controller
        )

        manager = TaskManager(factory)

        # run everything:
        await manager.execute_all(tasks)

    await browser.close()

    input('Press Enter to close the browser...')


if __name__ == "__main__":
    asyncio.run(main())
