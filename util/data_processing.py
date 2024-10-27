import json
from datetime import datetime
from typing import List, TypedDict
import unittest

data_file_path = "./data/mushroom.hi-val.v2.jsonl"
output_path = "./output/"
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

class SoftLabel(TypedDict):
    start: int 
    prob: float
    end: int

class HardLabel(TypedDict):
    start: int
    end: int

# This is the output labels, including hard and soft label
class Labels(TypedDict):
    soft_labels: List[SoftLabel]
    hard_labels: List[HardLabel]
# This is the output, contain the Input and Label
class Output(Input, Labels):
    pass


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
    return f"{output_path}output_{timestamp}.jsonl"  # Add timestamp to filename

# This is saving
def save_file_output(record: List[Output], output_file:str = _default_output_filename()):
    with open(output_file, mode='w', encoding='utf-8') as file:
        for entry in record:
            json_line = json.dumps(entry)  # 将字典转换为 JSON 字符串
            file.write(json_line + '\n')  # 每个 JSON 对象后添加换行符
    print(f"file have been saved to {output_file}")


# this is domain of test_function
class TestExample(unittest.TestCase):
    @unittest.skip("skip test_save_file_output")
    def test_save_file_output(self):
        data = load_file_jsonl()
        save_file_output(data)


if __name__ == "__main__":
    unittest.main()
