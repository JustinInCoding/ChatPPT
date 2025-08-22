import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from logger import LOG

class LLM:
    def __init__(self):
        self.client = ChatOpenAI(
            base_url="https://api.deepseek.com",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            model="deepseek-chat",
            temperature=0.7,
            max_tokens=1024,
        )
        LOG.add("daily_progress/llm_logs.log", rotation="1 MB", level="DEBUG")

    def load_prompt(self):
        """
        从文件加载系统提示语。
        """
        try:
            with open("prompts/formatter.txt", "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到提示文件 {self.prompt_file}!")
    def response(self, user_content):
        system_prompt = self.load_prompt()

        LOG.info("Starting response using DeepSeek model.")
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_content)
            ]

            response = self.client.invoke(messages)
            LOG.debug("DeepSeek response: {}", response)
            return response.content
        except Exception as e:
            LOG.error("An error occurred while generating the report: {}", e)
            raise
