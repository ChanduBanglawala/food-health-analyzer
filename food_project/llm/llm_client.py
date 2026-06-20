import os

from dotenv import load_dotenv


from langchain_openai import ChatOpenAI
load_dotenv()

class LLMClient:

    def __init__(self):

        self.llm = ChatOpenAI(
            model="nex-agi/nex-n2-pro:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            temperature=0.3,
            max_tokens=1000
        )

    def generate(self, prompt):

        response = self.llm.invoke(prompt)

        return response.content