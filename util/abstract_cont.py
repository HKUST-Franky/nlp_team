import re

def abstract_content(content: str):
    pattern = re.search(r'```(.*?)```', content, re.DOTALL)
    return pattern.group(1) if pattern else None

original = "OK, Here is the tagged text! This is the orginal ```<error>text.</error>```"
print(abstract_content(original))
