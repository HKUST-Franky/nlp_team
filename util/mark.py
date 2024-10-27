from typing import List, TypedDict
import unittest
from .data_processing import HardLabel


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
def fuck_off_marks(text: str, mark: Mark) -> List[str]:
    mark_start = mark.s
    mark_close = mark.e
    parts = []
    start = 0

    while True:
        index = text.find(mark_start, start)
        if index == -1:
            parts.append(text[start:])  # Append the remaining text if no more marks are found
            break
        before_start = text[start:index]  # Text before the mark
        start = index + len(mark_start)  # Update start position

        index_close = text.find(mark_close, start)
        if index_close == -1:
            print("no corresponding close mark!")
            parts.append(text[start:])  # Append the remaining text if no closing mark is found
            break
        middle = text[start:index_close]
        parts.append(before_start)
        parts.extend(["(", middle, ")"])  # Enclose the marked text in parentheses
        start = index_close + len(mark_close)  # Update start position to search for the next mark

    return parts

def plain_text(text_with_mark:str, mark:Mark)->str:
    res = text_with_mark.replace(mark.s, "")
    res = res.replace(mark.e, "")
    return res


#get starts & ends
def starts_and_ends(text: str, trunc_mark:Mark)-> List[HardLabel]:
    hard_label_lst = []
    text_segment = fuck_off_marks(text, trunc_mark)
    print(text_segment)
    start = 0
    new_label = HardLabel()
    for item in text_segment:
        if item == "(":
            new_label["start"] = start
        elif item ==")":
            new_label["end"] = start 
            hard_label_lst.append(list(new_label.values()))
            new_label = HardLabel()
        else:
            start += len(item)
    return hard_label_lst
     
     

# this is domain of test_function
class TestExample(unittest.TestCase):
    @unittest.skip("test")
    def test_mark(self):
        print(mark_table[0].s)
        print(mark_table[0].e)
        print(mark_table[0])

    def test_fuck_off(self):
        res = fuck_off_marks("shit <T>shit ?</T> <T>shit</T>", T)
        print(res)
        
    #@unittest.skip("skip test_fuck_off")
    def test_starts_and_ends(self):
        plain_text = "shit shit ? shit"
        text = "shit <T>shit ?</T> <T>shit</T>"
        should_be = [{"start": 5, "end": 10}]
        results = starts_and_ends(text, mark_table[0])
        print(results)
        print(plain_text[results[0]["start"]: results[0]["end"]])
        print(plain_text[results[1]["start"]: results[1]["end"]])
        print(f"should be{should_be}")
    @unittest.skip("test")
    def test_plain_text(self):
        text = "#shit <T>shit ?</T> shit#"
        print(plain_text(text, T))
        
    

if __name__ == "__main__":
    unittest.main()
