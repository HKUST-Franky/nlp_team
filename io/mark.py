from typing import List
import unittest

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
        if results == should_be:
            print("Match")

if __name__ == "__main__":
    unittest.main()
