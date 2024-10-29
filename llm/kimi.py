from .genetic import ChatLLM
from openai import OpenAI
import unittest
from typing import override
 

class Kimi(ChatLLM):
    def __init__(self, model_specific:str = "moonshot-v1-8k", api_key:str = "sk-0jCHBUd0o2XncKJPNncqmAN65KtB3nnLvyZjhW163rw7KjYz"):
        super().__init__("Kimi")
        self.api_key = api_key
        self.client = OpenAI(
            api_key = self.api_key,
            base_url = "https://api.moonshot.cn/v1",
        )
        self.specific_model = model_specific
    @override
    def ask(self, input_user:str = "Hello", input_system:str = "You are a Helpful assistant.")-> str:
        return super()._ask(input_user, input_system)

#Test
class TestExample(unittest.TestCase):
    def test_kimi(self):
        llm:ChatLLM = Kimi()
        res = llm.ask()
        print(res)

if __name__ == "__main__":
    unittest.main()