from .genetic import ChatLLM 
from openai import OpenAI
import unittest
from typing import override



class Llama(ChatLLM):
    def __init__(self, model_specific:str = "llama-3.1-8b-instant", api_key:str = "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"):
        super().__init__("Llama")
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
        llm:ChatLLM = Llama()
        res = llm.ask()
        print(res)
    
if __name__ == "__main__":
    unittest.main()
    