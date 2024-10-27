from .genetic import ChatLLM 
from openai import OpenAI
import unittest
from typing import override



class Qwen(ChatLLM):
    def __init__(self, model_specific:str = "qwen-plus", api_key:str = "sk-20a718b580bc42bebdc6fd9e736e04fb"):
        super().__init__("Qwen")
        self.api_key = api_key
        self.client = OpenAI(
            api_key = self.api_key,
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.specific_model = model_specific # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    @override
    def ask(self, input_user:str = "Hello", input_system:str = "You are a Helpful assistant.")-> str:
        return super()._ask(input_user, input_system)

#Test
class TestExample(unittest.TestCase):
    def test_qwen(self):
        llm:ChatLLM = Qwen()
        res = llm.ask()
        print(res)
    
if __name__ == "__main__":
    unittest.main()
    