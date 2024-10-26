import json
from datetime import datetime
from typing import List, TypedDict
from enum import Enum
import unittest


# to constrain the type of the dic
# This is data input
class Input(TypedDict):
    id: str 
    lang: str
    model_input: str
    model_output_text: str
    model_id:str
    model_output_logits: str
    model_output_tokens: str


# This is the output labels, including hard and soft label
class Label(TypedDict):
    soft_labels: str 
    hard_labels: str

# This is the output, contain the Input and Label
class Output(Input, Label):
    pass

data_file_path = "./data/mushroom.hi-val.v2.jsonl"  # Path to the JSONL file

# jsonl file to a dictionary.
# input the filepath, defaulted to be ./data/xxx.jsonl
# no check for the suffix of filename, should pay attention to .jsonl
def load_file_jsonl(file :str = data_file_path) -> str:
    data = []
    try:
        with open(file, mode='r', encoding='utf-8') as file:
            for line in file:
                # Parse each line as a JSON object
                json_obj = json.loads(line)
                data.append(json_obj)
    except FileNotFoundError:
        print(f"Error: File not found at {file}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. {e}")
    except Exception as e:
        print(f"Error: {e}")

    return data

# just_used in save_file_output
def _default_output_filename()-> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    return f"./output/output_{timestamp}.jsonl"  # Add timestamp to filename

# This is saving
def save_file_output(record: List[Output], output_file:str = _default_output_filename()):
    with open(output_file, mode='w', encoding='utf-8') as file:
        for entry in record:
            json_line = json.dumps(entry)  # 将字典转换为 JSON 字符串
            file.write(json_line + '\n')  # 每个 JSON 对象后添加换行符
    print(f"file have been saved to {output_file}")

# To register a Mark: T = Mark('T')
# To use it: T.s == "<T>"
# To use it: T.e == "</T>"
class Mark():
    def __init__(self, value: str):
        self.value = value
    def __str__(self):
        return f"Mark:{self.value}"
    @property
    def s(self):
        return f"<{self.value}>" 
    @property
    def e(self):
        return f"</{self.value}>"

T = Mark('T')
mark_table = [T]


# This is to strip the mark from text, and return split text segment.
def fuck_off_marks(text: str, mark: Mark)-> List[str]:
    mark_start = mark.s
    mark_close = mark.e 
    parts = []
    start = 0

    while True:
        index = text.find(mark_start, start)
        if index == -1:
            break
        before_start = text[:index]  # 标记前的部分
        start = index + len(mark_start)  # 更新起始位置
        
        index_close = text.find(mark_close, start)
        if index_close == -1:
            print("no corresponding close mark!")
            break
        middle = text[index + len(mark_start) : index_close]
        after_end = text[index_close + len(mark_close):]  # 标记后的部分
        parts.extend([before_start, middle, after_end])  # 添加切分结果
        start = index_close + len(mark_close)  # 更新起始位置以查找下一个标记

    return parts


# this is domain of test_function
class TestExample(unittest.TestCase):
    @unittest.skip("skip test_save_file_output")
    def test_save_file_output(self):
        data = load_file_jsonl()
        save_file_output(data)

    def test_mark(self):
        print(mark_table[0].s)
        print(mark_table[0].e)
        print(mark_table[0])

    #@unittest.skip("skip test_fuck_off")
    def test_fuck_off(self):
        text = "shit <T>shit </T> shit"
        should_be = ["shit ", "shit ", " shit"]
        results = fuck_off_marks(text, mark_table[0])
        print(results)
        print(f"should be{should_be}")


if __name__ == "__main__":
    unittest.main()
