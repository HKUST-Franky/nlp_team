from llm import qwen
import util.mark as m
import util.data_processing as dp
from typing import List


#step1. choose a model, you can specify api key, specific model i.e. qwen-plus etc.
# you can use gpt.GPT() as well
qwen = qwen.Qwen()

#prepare input
#You can load data from /input_data using dp.load_file_jsonl(filepath)
#pay attention to the file suffix: jsonl lllllllllllllllllll!
#You can specify the prompt_user as input and prompt_system as some instruction.
# **prompt_user = "hello hello hello hello hello hello hello hello hello hello"
# **prompt_system = "I will input you some text, add <T> and </T> in this text. you can randomly add it, but keep in mind they should be in pair and </T> should be after <t> all the time."
prompt_system = """
Given a passage, identify any <entity>, <relation>, <contradictory>, <subjective>, <unverifiable>, or <invented> errors in the passage. Mark each erroneous segment by enclosing it within the corresponding <error_type></error_type> tags. If there are no errors, return the passage with no tags. Any identified errors should be highlighted using the specified tags without altering the original text. Below are the error definitions followed by an example of the required format.

Definitions:

Entity Error (<entity>): A small part of a sentence, often an entity (e.g., location name), is incorrect (usually 1-3 words). Entity errors often involve noun phrases or nouns.
Relational Error (<relation>): A sentence is partially incorrect due to a small part (usually 1-3 words). Relational errors often involve verbs and are often the opposite of what they should be.
Contradictory Sentence Error (<contradictory>): A sentence where the entire content is contradicted by the given reference, meaning the sentence can be proven false due to a contradiction with information in the passage.
Invented Info Error (<invented>): Errors referring to entities that are not known or do not exist. This does not include fictional characters in books or movies. Invented errors include phrases or sentences with unknown entities or misleading information.
Subjective Sentence (<subjective>): An entire sentence or phrase that is subjective and cannot be verified, so it should not be included.
Unverifiable Sentence (<unverifiable>): A sentence where the whole sentence or phrase is unlikely to be factually grounded. Although it can be true, the sentence cannot be confirmed nor denied using the reference given or internet search. It is often something personal or private and hence cannot be confirmed.

##
Passage: Marooned on Mars is a science fiction novel aimed at a younger audience. It was written by Andy Weir and published by John C. Winston Co. in 1952, featuring illustrations by Alex Schomburg. It ended up having a readership of older boys despite efforts for it to be aimed at younger kids. The novel inspired the famous Broadway musical "Stranded Stars," which won six Tony Awards. The novel tells a story of being stranded on the Purple Planet. I wish the novel had more exciting and thrilling plot twists.
Edited: Marooned on Mars is a science fiction novel aimed at a younger audience.
It was written by <entity>Lester del Rey</entity> and published by John C. Winston Co. in 1952, featuring illustrations by Alex Schomburg.
<contradictory>It ended up having a readership of older boys despite efforts for it to be aimed at younger kids.</contradictory>
<invented>The novel inspired the famous Broadway musical "Stranded Stars," which won six Tony Awards.</invented>
The novel tells a story of being stranded on the <entity>Purple</entity> Planet.
<subjective>I wish the novel had more exciting and thrilling plot twists.</subjective>
##

Instructions: Now detect errors and include tags in the following passage as demonstrated in the example above. Use <error_type></error_type> tags around each identified error segment. If there are no errors, return the passage unchanged.

Passage:
The restoration of S\u00e1ndor Palace, also known as the Buda Castle, was completed in several phases. The most significant restoration took place between 1950 and 1961 under the supervision of Hungarian architects Gy\u0151z\u0151 Csapl\u00e1r and Lajos K\u00e9sm\u00e1rki. However, it's important to note that various parts of the palace continued to be restored and renovated throughout the decades following this period. Therefore, it is not accurate to pinpoint an exact completion date for the entire restoration project.

Edited:"""

input_lst = dp.load_file_jsonl()
prompt_user_lst = list(input["model_output_text"] for input in input_lst)
print(prompt_user_lst[0])

#I want to use my own mark like <mask>, how to do it?
#Just use m.Mark("mask") to make one.
# mask = Mark("mask")
# mask.s == <mask>
# mask.e == </mask>
#<entity>, <relation>, <contradictory>, <subjective>, <unverifiable>, or <invented>
entity = m.Mark("entity")
relation = m.Mark("relation")
contradictory = m.Mark("contradictory")
subjective = m.Mark("subjective")
unverifiable = m.Mark("unverifiable")
invented = m.Mark("invented")
#this should be erased in the output part
#user plain_text() in m package!
not_mask_lst = [entity, relation, contradictory, unverifiable, invented]

#my mask mark
mask = m.Mark("mask")

#get response by asking
#it's a str
#you can create a new class based on qwen or gpt to make your class and override the ask method to achieve your goal.
meow_lst = []
for prompt_user in prompt_user_lst:
    meow = qwen.ask(prompt_user, prompt_system)
    meow_lst.append(meow)

#erase not <mask> marks!
#you need to remove these not mask mark!
#because this will affect the function to get start and end label! i.e. starts_and_ends() func
plain_text_lst = []
for meow in meow_lst:
    for mark in not_mask_lst:
        meow = m.plain_text(meow, mark)
        plain_text_lst.append(meow)

#put then into output file
# corresponding input, list of output and the corresponding mark
# to give your a file with output!
def transform_text_list_with_mark_into_output_file(input_cor: List[str], text_lst: List[str], mark:m.Mark):
    output_lst = []
    input_and_output = zip(input_cor, text_lst)
    for tu in input_and_output:
        #get the hard_label i.e. [[12, 34], [34, 55] ...]
        #tu[1] text, tu[1] cor_input
        hard_labels = m.starts_and_ends(tu[1], mark)
        #TODO I dont know how to deal with the fucking soft labels, just blank
        #There soft label is empty, and hash_labels is just we got above.
        labels = dp.Labels(soft_labels=dp.SoftLabel(), hard_labels=hard_labels)
        #We need to put the input we use, too!
        input = dp.Input(model_input=tu[0], model_output_text=tu[1])
        #one instance
        output_one = dp.Output(input | labels)
        #add it to the list
        output_lst.append(output_one)
    #put them into a file!, you can specific the file_name actually
    dp.save_file_output(output_lst)

#do it!
# Here you should use your own mark! not m.T
transform_text_list_with_mark_into_output_file(prompt_user, meow_lst, mask)



#print(hard_labels) # "<T>"
#plain_text = mark.plain_text(meow, mark.T)
#def check(label, plain_text = plain_text):
#    return plain_text[label["start"]:label["end"]]
#
#something = map(check, hard_labels)
#print(list(something))