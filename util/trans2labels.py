import json
import pandas as pd
import re

# Manual check File for the output of the model
with open("test/de.json", "r", encoding="utf-8") as f:
    pred_dicts = json.load(f)

df = pd.read_json("input_data/de.jsonl", lines=True)
ref = df["model_output_text"]

labels_lst = []
for i in range(len(pred_dicts)):
    ele_list = pred_dicts[i]
    ref_sentence = ref[i]
    
    soft_lst = []
    hard_lst = []
    for ele in ele_list:
        start_idx = ref_sentence.find(ele)
        if start_idx != -1:
            end_idx = start_idx + len(ele)
            soft_labels = {"start": start_idx, "end": end_idx, "prob": float(1.0)}
            soft_lst.append(soft_labels)
            hard_labels = [start_idx, end_idx]
            hard_lst.append(hard_labels)
        else:
            print(f"Element: {ele} not found in the reference sentence.")
    labels_lst.append([soft_lst, hard_lst])

df_val = pd.read_json("input_data/en.jsonl", lines=True)
for i in range(len(df_val)):
    df_val.at[i, "soft_labels"] = labels_lst[i][0]
    df_val.at[i, "hard_labels"] = labels_lst[i][1]
# output file for results
df_val.to_json("test/rs_de.json", orient="records", lines=True)