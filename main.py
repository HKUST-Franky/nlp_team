from llm import qwen
import util.mark as m
import util.data_processing as dp
from typing import List
from datetime import datetime
import random


qwen = qwen.Qwen()
#TODO add this to class
model_name = "qwen"
#TODO modify this to use the file in prompt dir
prompt_fixed = """Given a passage, identify any entity, relation, contradictory, subjective, unverifiable, or invented errors in the passage. Mark each erroneous segment by enclosing it within the corresponding <error></error> tags. If there are no errors, return the passage with no tags. Any identified errors should be highlighted using the tag <error> without altering the original text. Below are the error definitions of the error types.

Definitions:

Entity Error: A small part of a sentence, often an entity (e.g., location name), is incorrect (usually 1-3 words). Entity errors often involve noun phrases or nouns.
Relational Error: A sentence is partially incorrect due to a small part (usually 1-3 words). Relational errors often involve verbs and are often the opposite of what they should be.
Contradictory Sentence Error: A sentence where the entire content is contradicted by the given reference, meaning the sentence can be proven false due to a contradiction with information in the passage.
Invented Info Error: Errors referring to entities that are not known or do not exist. This does not include fictional characters in books or movies. Invented errors include phrases or sentences with unknown entities or misleading information.
Subjective Sentence: An entire sentence or phrase that is subjective and cannot be verified, so it should not be included.
Unverifiable Sentence: A sentence where the whole sentence or phrase is unlikely to be factually grounded. Although it can be true, the sentence cannot be confirmed nor denied using the reference given or internet search. It is often something personal or private and hence cannot be confirmed.

##
Passage: Marooned on Mars is a science fiction novel aimed at a younger audience. It was written by Andy Weir and published by John C. Winston Co. in 1952, featuring illustrations by Alex Schomburg. It ended up having a readership of older boys despite efforts for it to be aimed at younger kids. The novel inspired the famous Broadway musical "Stranded Stars," which won six Tony Awards. The novel tells a story of being stranded on the Purple Planet. I wish the novel had more exciting and thrilling plot twists.
Edited: Marooned on Mars is a science fiction novel aimed at a younger audience.
It was written by <error>Lester del Rey</error> and published by John C. Winston Co. in 1952, featuring illustrations by Alex Schomburg.
<error>It ended up having a readership of older boys despite efforts for it to be aimed at younger kids.</error>
<error>The novel inspired the famous Broadway musical "Stranded Stars," which won six Tony Awards.</error>
The novel tells a story of being stranded on the <error>Purple</error> Planet.
<error>I wish the novel had more exciting and thrilling plot twists.</error>
##

Instructions: Now detect errors and include tag in the following passage as demonstrated in the example above. Use <error></error> tags around each identified error segment. If there are no errors, return the passage unchanged. Wait for my input after Passage:

Passage:
"""
# system_prompt
prompt_system = "You are a helpful agent."

#prompt for redo
prompt_redo = """
MY SWEET HEART, PLEASE DO NOT CHANGE THE ORIGINAL TEXT, JUST ADD TAGS, PLEASE. CAN YOU DO THAT AGAIN!
Your output should be like: original text <error>original text</error> original text
No extra text is needed. Just give me the answer.
It should be exactly the same, including spaces
This is the original:" + prompt_user
"""

#TODO modify this to read a list of file in a dir
file_list = ["ar", "de", "en", "es", "fi", "fr", "hi", "it", "sv", "zh"]


def load(file_name):
    #load file
    input_dir_path = "./input_data/" 
    suffix = ".jsonl"
    full_file_name = input_dir_path + file_name + suffix
    input_lst = dp.load_file_jsonl(full_file_name)
    
    return input_lst
    #get prompt

def ask_it(prompt_user_lst, mask):
    meow_lst = []
    for prompt_user in prompt_user_lst:
        ask = lambda x : qwen.ask(prompt_fixed + x, prompt_system)
        meow = ask(prompt_user)
        cnt = 0
        while m.plain_text(meow, mask) != prompt_user:
            #TODO modify this log info
            log_info = f"log info: original input:{prompt_user}, gpt output: {m.plain_text(meow, mask)}\n"
            log_info += f"difference: {m.find_char_differences(prompt_user, m.plain_text(meow, mask) )}"
            print(log_info)
            meow = ask(prompt_user + log_info + prompt_redo)        

            # to prevent loop
            #modify this part make it more concise
            cnt += 1
            if cnt > 10:
                meow = prompt_user
                break
            
        meow_lst.append(meow)
    return meow_lst


def transform_text_list_with_mark_into_output_file(input_cor: List[str], text_lst: List[str], mark:m.Mark):
    output_lst = []
    input_and_output = zip(input_cor, text_lst)
    for tu in input_and_output:
        #get the hard_label i.e. [[12, 34], [34, 55] ...]
        #tu[1] text, tu[1] cor_input
        hard_labels = m.starts_and_ends(tu[1], mark)
        #TODO I dont know how to deal with the fucking soft labels, just blank
        #There soft label is empty, and hash_labels is just we got above.
        soft_labels = []
        for hard_label in hard_labels:
            soft_labels.append(dp.SoftLabel({"start": hard_label[0], "prob": 1.0, "end":hard_label[1]}))
        labels = dp.Labels(soft_labels=soft_labels, hard_labels=hard_labels)
        #We need to put the input we use, too!
        #one instance
        output_one = dp.Output(tu[0] | labels)
        #add it to the list
        output_lst.append(output_one)
    #put them into a file!, you can specific the file_name actually

    timestampe = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "./output/" 
    output_filename = model_name + "_" + file_name + timestampe + str(random.randint(0, 1000))
    suffix = ".jsonl"
    full_output_filename = output_lst, output_dir + output_filename + suffix 
    dp.save_file_output(full_output_filename) 

def do(file_name):
    mask = m.Mark("error")
    input_lst = load(file_name)
    prompt_user_lst = list(input["model_output_text"] for input in input_lst)
    meow_lst = ask_it(prompt_user_lst)
    transform_text_list_with_mark_into_output_file(input_lst, meow_lst, mask)

for file_name in file_list:
    do(file_name)




