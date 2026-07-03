import os

from openai import OpenAI

from .prompts import SYSTEM_PROMPT


class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = "google/gemma-4-31b-it:free"

    def chat(self, message: str, user=None):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
                extra_headers={
                    "HTTP-Referer": "http://localhost:5174",
                    "X-Title": "Library Management System",
                },
            )

            return response.choices[0].message.content

        except Exception as e:
            import traceback
            traceback.print_exc()
            return str(e)