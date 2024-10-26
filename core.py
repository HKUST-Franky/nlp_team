import openai
import llm.gpt as gpt

# 替换为你的 OpenAI API 密钥
key2set = 'ILOVEYOUGPT'
gpt.set_open_ai_key(key2set)
gpt.model = "gpt-3.5-turbo"  # 或者使用 gpt-4，如果你有权限

# 示例提示
prompt = "请给我一个关于机器学习的简单介绍。"

# 获取响应
response = get_chatgpt_response(prompt)

# 输出结果
if response:
    print("ChatGPT的响应：")
    print(response)