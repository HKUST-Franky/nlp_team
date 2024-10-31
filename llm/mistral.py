from .genetic import ChatLLM 
from openai import OpenAI
import unittest
from typing import override



class Mistral(ChatLLM):
    def __init__(self, model_specific:str = "mixtral-8x7b-32768", api_key:str = "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"):
        super().__init__("Mistral")
        self.api_key = api_key
        self.client = OpenAI(
            api_key = self.api_key,
            base_url = "https://api.groq.com/openai/v1",
        )
        self.specific_model = model_specific # 模型列表：https://console.groq.com/docs/models
    @override
    def ask(self, input_user:str = "Hello", input_system:str = "You are a Helpful assistant.")-> str:
        return super()._ask(input_user, input_system)

#Test
class TestExample(unittest.TestCase):
    def test_qwen(self):
        llm:ChatLLM = Mistral()
        res = llm.ask()
        print(res)
    
if __name__ == "__main__":
    unittest.main()
    