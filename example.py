from llm import qwen
import util.mark as m
import util.data_processing as dp
from typing import List


#step1. choose a model, you can specify api key, specific model i.e. qwen-plus etc.
# you can use gpt.GPT() as well
qwen = qwen.Qwen()

#prepare input
#You can load data from /input_data using util.laod_file_jsonl(filepath)
#pay attention to the file suffix: jsonl lllllllllllllllllll!
#You can specify the prompt_user as input and prompt_system as some instruction.
prompt_user = "hello hello hello hello hello hello hello hello hello hello"
prompt_system = "I will input you some text, add <T> and </T> in this text. you can randomly add it, but keep in mind they should be in pair and </T> should be after <t> all the time."

#I want to use my own mark like <mask>, how to do it?
#Just use m.Mark("mask") to make one.
# mask = Mark("mask")
# mask.s == <mask>
# mask.e == </mask>


#get response by asking
#it's a str
#you can create a new class based on qwen or gpt to make your class and override the ask method to achieve your goal.
meow = qwen.ask(prompt_user, prompt_system)

#I did't repeat to ask qwen many times, i just manually repeat the same result 100 times
repeat_meow = [meow for i in range(100)]

#put then into output file
# corresponding input, list of output and the corresponding mark
# to give your a file with output!
def transform_text_list_with_mark_into_output_file(input_cor:str, text_lst: List[str], mark:m.Mark):
    output_lst = []
    for text in text_lst:
        #get the hard_label i.e. [[12, 34], [34, 55] ...]
        hard_labels = m.starts_and_ends(text, mark)
        #TODO I dont know how to deal with the fucking soft labels, just blank
        #There soft label is empty, and hash_labels is just we got above.
        labels = dp.Labels(soft_labels=dp.SoftLabel(), hard_labels=hard_labels)
        #We need to put the input we use, too!
        input = dp.Input(model_input=input_cor, model_output_text=text)
        #one instance
        output_one = dp.Output(input | labels)
        #add it to the list
        output_lst.append(output_one)
    #put them into a file!, you can specific the file_name actually
    dp.save_file_output(output_lst)

#do it!
# Here you should use your own mark! not m.T
transform_text_list_with_mark_into_output_file(prompt_user, repeat_meow, m.T)



#print(hard_labels) # "<T>"
#plain_text = mark.plain_text(meow, mark.T)
#def check(label, plain_text = plain_text):
#    return plain_text[label["start"]:label["end"]]
#
#something = map(check, hard_labels)
#print(list(something))