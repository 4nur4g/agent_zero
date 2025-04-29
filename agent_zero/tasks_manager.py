from typing import List, Any
import asyncio
from fastapi import WebSocket
from pyobjtojson import obj_to_json
import os
from browser_use.agent.service import Agent

import json
from typing import Any, Dict


def format_step_status(summary: Dict[str, Any]) -> str:
    """
    Given a dict like:
      {
        'url': 'https://example.com',
        'model_thoughts': 'Thinking…',
        'model_outputs': {'foo': 123},
        'model_actions': ['click', 'type']
      }
    Return a single Markdown‐style string, omitting any keys whose value is None or empty.
    """
    label_map = {
        "url": "URL",
        "model_thoughts": "Thoughts",
        "model_outputs": "Outputs",
        "model_actions": "Actions",
        "extracted_content": "Extracted Content",
    }

    parts = []
    for key, label in label_map.items():
        value = summary.get(key)
        # skip None, empty strings, empty lists/dicts
        if value is None or value == "" or (hasattr(value, "__len__") and len(value) == 0):
            continue

        if key == "url":
            # Markdown link
            url = str(value)
            parts.append(f"**{label}:** [{url}]({url})")
        else:
            # If it's a dict or list, dump it as JSON; else just string-ify
            if isinstance(value, (dict, list)):
                formatted = json.dumps(value, ensure_ascii=False)
            else:
                formatted = str(value)
            parts.append(f"**{label}:** {formatted}")

    # join with blank lines so it’s nicely separated in the UI
    return "\n\n".join(parts)


def get_real_time_update_function(socket: WebSocket = None):
    async def record_activity(agent_obj: Agent):
        website_html = None
        website_screenshot = None
        urls_json_last_elem = None
        model_thoughts_last_elem = None
        model_outputs_json_last_elem = None
        model_actions_json_last_elem = None
        extracted_content_json_last_elem = None

        print('--- ON_STEP_START HOOK ---')
        website_html: str = await agent_obj.browser_context.get_page_html()
        website_screenshot: str = await agent_obj.browser_context.take_screenshot()

        print('--> History:')
        if hasattr(agent_obj, 'state'):
            history = agent_obj.state.history
        else:
            history = None

        model_thoughts = obj_to_json(obj=history.model_thoughts(), check_circular=False)

        # print("--- MODEL THOUGHTS ---")
        if len(model_thoughts) > 0:
            model_thoughts_last_elem = model_thoughts[-1]
        # prettyprinter.cpprint(model_thoughts_last_elem)

        # print("--- MODEL OUTPUT ACTION ---")
        model_outputs = agent_obj.state.history.model_outputs()
        model_outputs_json = obj_to_json(obj=model_outputs, check_circular=False)

        if len(model_outputs_json) > 0:
            model_outputs_json_last_elem = model_outputs_json[-1]
        # prettyprinter.cpprint(model_outputs_json_last_elem)

        # print("--- MODEL INTERACTED ELEM ---")
        model_actions = agent_obj.state.history.model_actions()
        model_actions_json = obj_to_json(obj=model_actions, check_circular=False)

        if len(model_actions_json) > 0:
            model_actions_json_last_elem = model_actions_json[-1]
        # prettyprinter.cpprint(model_actions_json_last_elem)

        # print("--- EXTRACTED CONTENT ---")
        extracted_content = agent_obj.state.history.extracted_content()
        extracted_content_json = obj_to_json(obj=extracted_content, check_circular=False)
        if len(extracted_content_json) > 0:
            extracted_content_json_last_elem = extracted_content_json[-1]
        # prettyprinter.cpprint(extracted_content_json_last_elem)

        # print("--- URLS ---")
        urls = agent_obj.state.history.urls()
        # prettyprinter.cpprint(urls)
        urls_json = obj_to_json(obj=urls, check_circular=False)

        if len(urls_json) > 0:
            urls_json_last_elem = urls_json[-1]
        # prettyprinter.cpprint(urls_json_last_elem)

        model_step_summary = {
            # 'website_html': website_html,
            # 'website_screenshot': website_screenshot,
            # 'url': urls_json_last_elem,
            'model_thoughts': model_thoughts_last_elem,
            # 'model_outputs': model_outputs_json_last_elem,
            # 'model_actions': model_actions_json_last_elem,
            # 'extracted_content': extracted_content_json_last_elem,
        }

        print('--- MODEL STEP SUMMARY ---')
        # prettyprinter.cpprint(model_step_summary)
        print("Socket inside update function: ", socket)
        if socket:
            print("Sending update to socket")
            asyncio.create_task(socket.send_json({
                "type": "agent_zero_updates",
                "message": format_step_status(model_step_summary)
            }))

    return record_activity


class AgentFactory:
    """
    Responsible for constructing Agents.
    If you need to customize agent creation (e.g. add metrics, hooks, decorators),
    you do it here without touching execution logic.
    """

    def __init__(self, llm, sensitive_data, browser, browser_context, save_path: str, controller, use_vision=False,
                 socket=None, save_playwright_script_path=None):
        self.llm = llm
        self.sensitive_data = sensitive_data
        self.browser = browser
        self.browser_context = browser_context
        self.save_path = save_path
        self.controller = controller
        self.use_vision = use_vision
        self.socket = socket
        self.save_playwright_script_path = save_playwright_script_path

    def create(self, task):
        task_str = "\n".join(task.get("subtasks", []))
        message_ctx = task.get("title", "")

        base_kwargs = {
            "llm": self.llm,
            "save_conversation_path": self.save_path,
            "sensitive_data": self.sensitive_data,
            "browser": self.browser,
            "browser_context": self.browser_context,
            "task": task_str,
            "message_context": message_ctx,
            "controller": self.controller,
            "use_vision": self.use_vision,
            # Add Playwright script generation path
            "save_playwright_script_path": os.path.join(self.save_playwright_script_path,
                                                        f"playwright_script_{message_ctx.replace(' ', '_')}.py"),
            "use_vision_for_planner": True,
            "planner_interval": 4,
        }

        # collect everything else (including a possible "use_vision" override)
        extra_kwargs = {
            k: v for k, v in task.items()
            if k not in ("title", "subtasks")
        }

        # merging: keys in extra_kwargs will overwrite base_kwargs
        all_kwargs = base_kwargs.copy()
        all_kwargs.update(extra_kwargs)

        final_agent = Agent(**all_kwargs)
        final_agent.socket = self.socket

        return {"agent": final_agent, "socket": self.socket}


class TaskManager:
    """
    Coordinates running a collection of tasks.
    Keeps track of numbering, result collection, logging, etc.
    """

    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory

    async def execute_all(self, tasks: List[str]) -> List[Any]:
        results = []
        for idx, task in enumerate(tasks, start=1):
            agent = self.agent_factory.create(task)["agent"]
            socket = self.agent_factory.create(task)["socket"]

            async def dummy_update(x):
                print("can't send updates 😭")

            real_time_update = (
                get_real_time_update_function(socket=socket)
                if socket
                else dummy_update
            )

            result = await agent.run(on_step_start=real_time_update)
            print(f"[Task {idx}] Result:", result)
            results.append(result)
        return results
