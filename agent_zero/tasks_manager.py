from typing import List, Any
import asyncio

from browser_use.agent.service import Agent


# --- agent_factory.py ---------------------------------------
class AgentFactory:
    """
    Responsible for constructing Agents.
    If you need to customize agent creation (e.g. add metrics, hooks, decorators),
    you do it here without touching execution logic.
    """

    def __init__(self, llm, sensitive_data, browser, browser_context, save_path: str, controller, use_vision=False, planner_llm=None):
        self.llm = llm
        self.sensitive_data = sensitive_data
        self.browser = browser
        self.browser_context = browser_context
        self.save_path = save_path
        self.controller = controller
        self.use_vision = use_vision
        self.planner_llm = planner_llm

    def create(self, task) -> "Agent":
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
            "planner_llm": self.planner_llm if self.planner_llm else self.llm,  # Separate model for planning
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

        return final_agent


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
            agent = self.agent_factory.create(task)
            result = await agent.run()
            print(f"[Task {idx}] Result:", result)
            results.append(result)
        return results
