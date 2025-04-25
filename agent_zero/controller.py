import base64
import os

from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller


def get_controller(socket=None, queue=None) -> Controller:
    """
    Construct a Controller whose `ask_human` action will:
    1) send a prompt (and screenshot) over `socket`
    2) wait on `queue.get()` for the user's reply
    3) fallback to console input if socket/queue aren't provided
    """
    controller = Controller(exclude_actions=['search_google'])

    @controller.action('Ask user for information')
    async def ask_human(question: str, browser: BrowserContext) -> ActionResult:
        # 1) capture screenshot
        screenshot_b64 = await browser.take_screenshot()

        # make sure the directory exists & save a local copy if you need it
        os.makedirs("screenshots", exist_ok=True)
        with open("screenshots/my_capture.png", "wb") as f:
            f.write(base64.b64decode(screenshot_b64))

        # 2) if we have a live WebSocket + queue, use them
        if socket is not None and queue is not None:
            try:
                # a) send the prompt (and screenshot) to the front-end
                await socket.send_json({
                    "type": "prompt",
                    "prompt": question,
                    "screenshot": screenshot_b64,
                })
                # b) wait here until the front-end does:
                #    socket.send(JSON.stringify({ type:"response", text:"<their answer>" }))
                answer = await queue.get()
            except Exception as e:
                print(f"Error sending prompt: {e}")
                answer = input(f"\n{question}\nInput: ")

        else:
            # 3) fallback for CLI
            answer = input(f"\n{question}\nInput: ")

        # wrap up and return
        return ActionResult(extracted_content=answer)

    return controller
