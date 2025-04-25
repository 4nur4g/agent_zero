from typing import List, Any
import asyncio

from browser_use.agent.service import Agent


class AgentFactory:
    """
    Responsible for constructing Agents.
    If you need to customize agent creation (e.g. add metrics, hooks, decorators),
    you do it here without touching execution logic.
    """
    def __init__(self, llm, sensitive_data, browser, browser_context, save_path: str, controller):
        self.llm = llm
        self.sensitive_data = sensitive_data
        self.browser = browser
        self.browser_context = browser_context
        self.save_path = save_path
        self.controller = controller

    def create(self, task) -> "Agent":
        return Agent(
            llm=self.llm,
            save_conversation_path=self.save_path,
            sensitive_data=self.sensitive_data,
            browser=self.browser,
            browser_context=self.browser_context,
            task='\n'.join(task["subtasks"]),
            message_context=task["title"],
            controller=self.controller
        )


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

