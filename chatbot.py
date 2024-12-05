import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('UPDATED_API_KEY')


class AIAgent:
    def __init__(self):
        self.api_key = API_KEY
        self.client = Groq(api_key=self.api_key)
        self.messages = [
            {
                "role": "system",
                "content": "Linux AI Agent which is expert to teach Beginner Linux and Generate bash Scripts accurately"
            }
        ]

    def draft_message(self, content, role='user'):
        return {
            "role": role,
            "content": content
        }

    def get_response(self, prompt):
        self.messages.append(self.draft_message(prompt))
        
        chat_completion = self.client.chat.completions.create(
            temperature=1.0,
            n=1,
            model="mixtral-8x7b-32768",
            max_tokens=10000,
            messages=self.messages
        )
        response = chat_completion.choices[0].message.content
        # print("Agent Response:-> ", response)
        self.messages.append(self.draft_message(response, role='assistant'))
        
        return response
    
    
print(API_KEY)

# Backup Model
# mixtral-8x7b-32768
# Max Toxens = 10000

# New Mode
# llama-3.1-70b-versatile
# Max Toxens = 8000