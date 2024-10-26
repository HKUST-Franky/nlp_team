import json
from datetime import datetime

data_file_path = "./data/mushroom.hi-val.v2.jsonl"  # Path to the JSONL file

"""json_keys(['id', 'lang', 'model_input', 'model_output_text', 'model_id'])
out_put_key should have more include:
(['soft_labels', 'hard_labels', 'model_output_logits', 'model_output_tokens'])"""
# jsonl file to a dictionary.
def load_file_jsonl(file = data_file_path):
    data = []
    try:
        with open(file, mode='r', encoding='utf-8') as file:
            for line in file:
                # Parse each line as a JSON object
                json_obj = json.loads(line)
                data.append(json_obj)

        # Print the loaded data
    except FileNotFoundError:
        print(f"Error: File not found at {file}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. {e}")
    except Exception as e:
        print(f"Error: {e}")

    return data

def default_output_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    return f"./output/output_{timestamp}.jsonl"  # Add timestamp to filename

def save_file_output(record, output_file = default_output_filename()):
    for dic in data:
        if not is_valid_format(dic): 
            print("Your output diction is not valid! Check your keys!")
    with open(output_file, mode='w', encoding='utf-8') as file:
        for entry in record:
            json_line = json.dumps(entry)  # 将字典转换为 JSON 字符串
            file.write(json_line + '\n')  # 每个 JSON 对象后添加换行符
    print(f"file have been saved to {output_file}")

"""json_keys(['id', 'lang', 'model_input', 'model_output_text', 'model_id'])
out_put_key should have more include:
(['soft_labels', 'hard_labels', 'model_output_logits', 'model_output_tokens'])"""

def is_valid_format(data):
    key1 = ['id', 'lang', 'model_input', 'model_output_text', 'model_id']
    key2 = ['soft_labels', 'hard_labels', 'model_output_logits', 'model_output_tokens']
    key2check = key1 + key2
    if not isinstance(data, dict):
        return False
    
    # 检查必需的键和它们的类型
    for key in key2check:
        if key in data:
            continue
        else:
            return False
    return True    

#
mark_table = ['<T>']
def processing_mark(text, mark):
    # 使用标记分割文本
    start_tag = mark
    end_tag = mark.replace('<', '</')

    parts = []
    current_part = ''
    inside_tag = False

    i = 0
    while i < len(text):
        if text.startswith(start_tag, i):
            if current_part:
                parts.append(current_part.strip())
                current_part = ''
            inside_tag = True
            i += len(start_tag)
        elif text.startswith(end_tag, i):
            inside_tag = False
            i += len(end_tag)
        else:
            if not inside_tag:
                current_part += text[i]
            i += 1

    if current_part:
        parts.append(current_part.strip())

    return parts

# 示例使用
text = "hello <T>shit</T> fuck you"
result = processing_mark(text, '<T>')
print(result) 

#try
#data = load_file_jsonl()
#save_file_output(data)