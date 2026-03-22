import json
import google.generativeai as genai
from app.core.config import settings


genai.configure(api_key=settings.GEMINI_API_KEY)


class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
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
        response = await self.model.generate_content_async(prompt)
        text = response.text.strip()

        # Clean response if markdown code blocks exists
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        tasks = json.loads(text)
        return tasks