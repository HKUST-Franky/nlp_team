from llm import qwen

#step1. choose a model, you can specify api key, specific model i.e. qwen-plus etc.
qwen = qwen.Qwen()

#prepare input
prompt_user = "请给我一个关于机器学习的简单介绍。"
prompt_system = "你是一只小猫咪"

#get response by asking
meow = qwen.ask(prompt_user, prompt_system)
print(meow)