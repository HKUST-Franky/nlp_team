from llm import qwen
import util.mark as m
import util.data_processing as dp
from typing import List
from datetime import datetime
import random


qwen = qwen.Qwen()
model_name = "qwen"
prompt_system = """Given a passage, identify any entity, relation, contradictory, subjective, unverifiable, or invented errors in the passage. Mark each erroneous segment by enclosing it within the corresponding <error></error> tags. If there are no errors, return the passage with no tags. Any identified errors should be highlighted using the tag <error> without altering the original text. Below are the error definitions of the error types.

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
file_list = ["ar", "de", "en", "es", "fi", "fr", "hi", "it", "sv", "zh"]

# I want to sleep. I dont want to waste more time!
def do(file_name):
    input_lst = dp.load_file_jsonl("./input_data/" + file_name + ".jsonl")
    prompt_user_lst = list(input["model_output_text"] for input in input_lst)
    mask = m.Mark("error")

    meow_lst = []
    for prompt_user in prompt_user_lst:
        meow = qwen.ask(prompt_user, prompt_system)
        plain_meow = m.plain_text(meow, mask)
        while len(plain_meow) != len(prompt_user):
            log_info = f"log info: original input:{prompt_user}, gpt output: {meow}"
            print(log_info)
            to_add = "MY SWEET HEART, PLEASE DO NOT CHANGE THE ORIGINAL TEXT, JUST ADD TAGS, PLEASE. CAN YOU DO THAT AGAIN!"
            to_add_2 = "Should be like something original text <error>original text</error> original text"
            meow = qwen.ask(prompt_user + log_info + to_add, prompt_system)        
        meow_lst.append(meow)

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
        dp.save_file_output(output_lst, "./output/" + model_name + "_" + file_name + timestampe + str(random.randint(0, 1000)) + ".jsonl") 

    #do it!
    # Here you should use your own mark! not m.T
    transform_text_list_with_mark_into_output_file(input_lst, meow_lst, mask)
for file_name in file_list:
    do(file_name)
