from llm import qwen

#step1. choose a model, you can specify api key, specific model i.e. qwen-plus etc.
qwen = qwen.Qwen()

#prepare input
prompt_user = "hello hello hello hello hello hello hello hello hello hello"
prompt_system = "I will input you some text, add <T> and </T> in this text. you can randomly add it, but keep in mind they should be in pair and </T> should be after <t> all the time."

#get response by asking
meow = qwen.ask(prompt_user, prompt_system)
print(meow)