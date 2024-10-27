from llm import qwen
import util.mark as mark
import util.data_processing as dp


#step1. choose a model, you can specify api key, specific model i.e. qwen-plus etc.
qwen = qwen.Qwen()

#prepare input
prompt_user = "hello hello hello hello hello hello hello hello hello hello"
prompt_system = "I will input you some text, add <T> and </T> in this text. you can randomly add it, but keep in mind they should be in pair and </T> should be after <t> all the time."

#get response by asking
meow = qwen.ask(prompt_user, prompt_system)
print(meow)
hard_labels = mark.starts_and_ends(meow, mark.T)
labels = dp.Labels(soft_labels=dp.SoftLabel(), hard_labels=hard_labels)
input = dp.Input(model_input=prompt_user, model_output_text=meow)
output_one = dp.Output(input | labels)
dp.save_file_output([output_one])




#print(hard_labels) # "<T>"
#plain_text = mark.plain_text(meow, mark.T)
#def check(label, plain_text = plain_text):
#    return plain_text[label["start"]:label["end"]]
#
#something = map(check, hard_labels)
#print(list(something))