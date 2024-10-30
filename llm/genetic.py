from typing import List, TypedDict
import json

#this class is for input and output collection
#default one

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

class ResponseBody(TypedDict):
    id: str
    choices: List[ChoiceBody]
    created: int
    model: str
    object: str
    service_tier: str  #TBD
    system_fingerprint: str #TBD
    usage: TypedDict

class ChatLLM():
    def __init__(self):
        self.model_id = "default" 
    def __init__(self, model_id):
        self.model_id = model_id
    def ask(self, input_user:str, input_system:str)-> str:
        return "DEFAULT"
    def _ask(self, input_user: str = "Hello", input_system:str = 'You are a helpful assistant.')-> str:
        completion = self.client.chat.completions.create(
            model = self.specific_model,
            messages=[
                {'role': 'system', 'content': input_system},
                {'role': 'user', 'content': input_user}
            ],
            temperature=0.1,
        )
        json_str = completion.model_dump_json()

        try:
            response:ResponseBody = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        response:ChoiceBody = response['choices'][0] #TODO multiple response? multiple message?
        response:MessageBody = response['message']['content']
        return response