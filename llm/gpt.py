from openai import OpenAI
from llm import ChatLLM
from typing import override
import unittest


class GPT(ChatLLM):
    def __init__(self, model_specific:str = "gpt-3.5-turbo", api_key:str = "TBD"):
        super().__init__("ChatGPT")
        self.api_key= api_key
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
