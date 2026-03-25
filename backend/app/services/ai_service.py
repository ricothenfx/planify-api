import json
from google import genai
from app.core.config import settings


client = genai.Client(api_key=settings.GEMINI_API_KEY)


class AIService:
    async def generate_tasks(
        self,
        project_name: str,
        project_description: str | None,
    ) -> list[dict]:
        prompt = f"""
            You are a project management assistant. Generate a practical task list for the following project.

            Project Name: {project_name}
            Project Description: {project_description or "No description provided"}

            Generate 5-8 tasks that are specific, actionable, and relevant to this project.
            Distribute priority realistically:
            - "high": only for critical/blocking tasks (max 2-3 tasks)
            - "medium": for important but not blocking tasks (most tasks)
            - "low": for nice-to-have or final polish tasks (at least 1 task)

            Respond ONLY with a valid JSON array. No explanation, no markdown, no code blocks.
            Each task must have exactly these fields:
            - "title": short task title (max 100 chars)
            - "description": detailed description of what needs to be done
            - "priority": one of "low", "medium", "high"

            Example format:
            [
            {{
                "title": "Task title here",
                "description": "Detailed description here",
                "priority": "medium"
            }}
            ]
            """
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        text = response.text.strip()

        # Clean response if markdown code blocks exists
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        tasks = json.loads(text)
        return tasks
    
    async def suggest_next_actions(
        self,
        task_title: str,
        task_description: str | None,
        new_status: str,
        project_name: str,
    ) -> list[str]:
        prompt = f"""
    You are a project management assistant. A task status has been updated.

    Project: {project_name}
    Task: {task_title}
    Description: {task_description or "No description"}
    New Status: {new_status}

    Give 2-3 short, actionable suggestions for what the team should do next.
    Be specific and practical.

    Respond ONLY with a valid JSON array of strings. No explanation, no markdown.
    Example: ["suggestion 1", "suggestion 2", "suggestion 3"]
    """
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        text = response.text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        return json.loads(text)