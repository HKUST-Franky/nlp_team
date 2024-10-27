from llm import qwen
import util.mark as m
import util.data_processing as dp
from typing import List


#step1. choose a model, you can specify api key, specific model i.e. qwen-plus etc.
qwen = qwen.Qwen()

#prepare input
prompt_user = "hello hello hello hello hello hello hello hello hello hello"
prompt_system = "I will input you some text, add <T> and </T> in this text. you can randomly add it, but keep in mind they should be in pair and </T> should be after <t> all the time."

#get response by asking
meow = qwen.ask(prompt_user, prompt_system)

repeat_meow = [meow for i in range(100)]
#put then into output file
def transform_text_list_with_mark_into_output_file(input_cor:str, text_lst: List[str], mark:m.Mark):
    output_lst = []
    for text in text_lst:
        hard_labels = m.starts_and_ends(text, m.T)
        #TODO I dont know how to deal with the fucking soft labels, just blank
        labels = dp.Labels(soft_labels=dp.SoftLabel(), hard_labels=hard_labels)
        input = dp.Input(model_input=input_cor, model_output_text=text)
        output_one = dp.Output(input | labels)
        output_lst.append(output_one)
    dp.save_file_output(output_lst)

transform_text_list_with_mark_into_output_file(prompt_user, repeat_meow, m.T)



#print(hard_labels) # "<T>"
#plain_text = mark.plain_text(meow, mark.T)
#def check(label, plain_text = plain_text):
#    return plain_text[label["start"]:label["end"]]
#
#something = map(check, hard_labels)
#print(list(something))