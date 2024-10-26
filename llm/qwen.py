import os
from llm import ChatLLM
from openai import OpenAI
from typing import List, TypedDict
import unittest
import json

class MessageBody(TypedDict):
    content: str
    refusal: str #TBD
    role: str
    audio: str #TBD
    function_call: str #TBD
    tool_calls: str #TBD

class ChoiceBody(TypedDict):
    finish_reason: str 
    index: int
    logprobs: str #TBD
    message: MessageBody

class QwenResponseBody(TypedDict):
    id: str
    choices: List[ChoiceBody]
    created: int
    model: str
    object: str
    service_tier: str  #TBD
    system_fingerprint: str #TBD
    usage: TypedDict

class Qwen(ChatLLM):
    def __init__(self):
        super().__init__("Qwen")
        self.api_key="sk-20a718b580bc42bebdc6fd9e736e04fb"
        #sk-20a718b580bc42bebdc6fd9e736e04fb
        self.client = OpenAI(
            api_key = self.api_key,
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.specific_model = "qwen-plus"   # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        self.last_response = ""

    def ask(self, input_user: str = "Hello", input_system = 'You are a helpful assistant.')-> str:
        completion = self.client.chat.completions.create(
            model = self.specific_model,
            messages=[
                {'role': 'system', 'content': input_system},
                {'role': 'user', 'content': input_user}
            ],
        )
        json_str = completion.model_dump_json()

        try:
            response:QwenResponseBody = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        response:ChoiceBody = response['choices'][0] #TODO multiple response? multiple message?
        response:MessageBody = response['message']['content']
        return response


#Test
class TestExample(unittest.TestCase):
    def test_qwen(self):
        llm:ChatLLM = Qwen()
        res = llm.ask()
        print(res)
    
if __name__ == "__main__":
    unittest.main()
    