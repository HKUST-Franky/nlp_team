#this class is for input and output collection
#default one
class ChatLLM():
    def __init__(self):
        self.model_id = "default" 
    def __init__(self, model_id):
        self.model_id = model_id
    def ask(input: str)-> str:
        return "hello"