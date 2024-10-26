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

def fuck_off_marks(text, mark):
    mark_close = "</" + mark[1:-1] + ">"
    parts = []
    start = 0

    while True:
        index = text.find(mark, start)
        if index == -1:
            break
        before_start = text[:index]  # 标记前的部分
        start = index + len(mark)  # 更新起始位置
        
        index_close = text.find(mark_close, start)
        if index_close == -1:
            print("no corresponding close mark!")
            break
        middle = text[index + len(mark) : index_close]
        after_end = text[index_close + len(mark_close):]  # 标记后的部分
        parts.append((before_start, middle, after_end))  # 添加切分结果
        start = index_close + len(mark_close)  # 更新起始位置以查找下一个标记

    return parts

#try
#text = "shit <T>shit </T> shit"
#results = fuck_off_marks(text, "<T>")
#print(results)

#try
#data = load_file_jsonl()
#save_file_output(data)