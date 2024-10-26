from openai import OpenAI

gpt_api_key = 'YOUR_API_KEY'
model = "gpt-3.5-turbo"  # 或者使用 gpt-4，如果你有权限

client = OpenAI(api_key=gpt_api_key)

def set_open_ai_key(key):
    global gpt_api_key
    gpt_api_key = key
    
def set_open_ai_model(model2set):
    global model
    model = model2set

def get_chatgpt_response(prompt, model_selected = model):
    try:
        response = client.chat.completions.create(model=model_selected,  
        messages=[
            {"role": "user", "content": prompt}
        ])
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

toprint = get_chatgpt_response("how are you?")
print(f"response:{toprint}")