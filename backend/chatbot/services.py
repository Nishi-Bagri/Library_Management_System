import os
import json

from openai import OpenAI, RateLimitError

from .prompts import SYSTEM_PROMPT
from .tool_registry import TOOLS
from .tool_dispatcher import TOOL_FUNCTIONS


class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        
        #self.model = "google/gemma-4-31b-it:free"
                   
        self.model = "openai/gpt-oss-120b:free"

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
                tools=TOOLS,
                tool_choice="auto",
                extra_headers={
                    "HTTP-Referer": "http://localhost:5174",
                    "X-Title": "Library Management System",
                },
            )

            assistant_message = response.choices[0].message

            
            if not assistant_message.tool_calls:
                return assistant_message.content

            
            tool_call = assistant_message.tool_calls[0]

            tool_name = tool_call.function.name

            arguments = json.loads(tool_call.function.arguments)

            print("Tool:", tool_name)
            print("Arguments:", arguments)

            tool = TOOL_FUNCTIONS.get(tool_name)

            if tool is None:
                return f"Unknown tool: {tool_name}"

            
            result = tool(**arguments)

            print("Result:", result)

            
            second_response = self.client.chat.completions.create(
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
                    assistant_message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    },
                ],
                extra_headers={
                    "HTTP-Referer": "http://localhost:5174",
                    "X-Title": "Library Management System",
                },
            )

            return second_response.choices[0].message.content

        except RateLimitError:
            return (
                "⚠️ The AI service is currently busy because the free model "
                "has reached its request limit. Please wait a minute and try again."
            )

        except Exception as e:
            import traceback

            traceback.print_exc()

            return f"Unexpected error: {str(e)}"