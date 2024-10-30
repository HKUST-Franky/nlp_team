from openai import OpenAI
from .genetic import ChatLLM
from typing import override
import unittest


class GPT(ChatLLM):
    def __init__(self, model_specific:str = "gpt-4o", api_key:str = "TBD"):
        super().__init__("ChatGPT")
        self.api_key= "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"
        self.client = OpenAI(api_key=self.api_key)
        self.specific_model = model_specific 

    @override
    def ask(self, input_user:str = "Hello", input_system:str = "You are a Helpful assistant.")-> str:
        return super()._ask(input_user, input_system)


#Test
class TestExample(unittest.TestCase):
    def test_gpt(self):
        llm:ChatLLM = GPT()
        res = llm.ask()
        print(res)
    
if __name__ == "__main__":
    unittest.main()
