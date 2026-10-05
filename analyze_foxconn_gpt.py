from dataset import FoxconnDataset
import json
import numpy as np
from sklearn.metrics import f1_score

'''
| Task | Primary metric |
|---|---|
| Choice | Accuracy |
| Noul | F1 + Accuracy |
| Score | MAE |
| All | Output validity |
'''

gpt_pricing_input = 5/1000000 # 5 dollars per 1 million tokens 
gpt_pricing_output = 30/1000000 # 30 dollars per 1 million tokens

foxconn_choice = FoxconnDataset(type='choice', folder_path='dataset/starter_tasks/choice_ticket_routing.jsonl')
foxconn_noul = FoxconnDataset(type='noul', folder_path='dataset/starter_tasks/noul_release_gate.jsonl')
foxconn_score = FoxconnDataset(type='score', folder_path='dataset/starter_tasks/score_incident_priority.jsonl')

foxconn_choice_result_file = "./output_gpt/exp/foxconn/foxconn_choice_result.jsonl"
foxconn_choice_timer_file = "./output_gpt/exp/foxconn/foxconn_choice_timer.jsonl"
foxconn_noul_result_file = "./output_gpt/exp/foxconn/foxconn_noul_result.jsonl" 
foxconn_noul_timer_file = "./output_gpt/exp/foxconn/foxconn_noul_timer.jsonl"
foxconn_score_result_file = "./output_gpt/exp/foxconn/foxconn_score_result.jsonl"
foxconn_score_timer_file = "./output_gpt/exp/foxconn/foxconn_score_timer.jsonl"

input_token_count = 0
output_token_count = 0

print("Starting analysis for Foxconn dataset on GPT 5.5 output...")

##################
# choice 
##################

predicted = []
with open(foxconn_choice_result_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            predicted.append(answers[key])
        
        usage = result['usage']
        for key in usage.keys():
            input_tokens = usage[key]['prompt_tokens']
            output_tokens = usage[key]['completion_tokens']
            input_token_count += input_tokens
            output_token_count += output_tokens

            
lable = []
for sample in foxconn_choice:
    questions = sample.questions
    for question in questions:
        lable.append(question.label)

if len(predicted) != len(lable):
    print("Warning: The number of predicted labels does not match the number of true labels.")
tmp = []
for p, t in zip(predicted, lable):
    #print(f"Predicted: {p}, True: {t}")
    tmp.append(p == t)
accuracy = np.mean(tmp).item()

latency = 0
# only one line list of latency values is expected
with open(foxconn_choice_timer_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        latency = np.mean(list(result)).item()

print(f"Accuracy Choice: {accuracy}")
print(f"Choice Latency: {latency}")

##################
# noul
##################
predicted = []
with open(foxconn_noul_result_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            predicted.append(True if answers[key] == 'True' else False)
        
        usage = result['usage']
        for key in usage.keys():
            input_tokens = usage[key]['prompt_tokens']
            output_tokens = usage[key]['completion_tokens']
            input_token_count += input_tokens
            output_token_count += output_tokens
lable = []
for sample in foxconn_noul:
    questions = sample.questions
    for question in questions:
        lable.append(question.label)

if len(predicted) != len(lable):
    print("Warning: The number of predicted labels does not match the number of true labels.")
tmp = []
for p, t in zip(predicted, lable):
    # print(f"Predicted: {p}, True: {t}")
    tmp.append(p == t)

# compute accuracy for noul
accuracy = np.mean(tmp).item()
print(f"Accuracy Noul: {accuracy}")
# compute F1 score for noul
f1 = f1_score(lable, predicted)
print(f"F1 Noul: {f1}")

latency = 0
# only one line list of latency values is expected
with open(foxconn_noul_timer_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        latency = np.mean(list(result)).item()

print(f"Noul Latency: {latency}")

##################
# score
##################
predicted = []
with open(foxconn_score_result_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            predicted.append(float(answers[key]))

        usage = result['usage']
        for key in usage.keys():
            input_tokens = usage[key]['prompt_tokens']
            output_tokens = usage[key]['completion_tokens']
            input_token_count += input_tokens
            output_token_count += output_tokens

lable = []
for sample in foxconn_score:
    questions = sample.questions
    for question in questions:
        lable.append(question.label)

if len(predicted) != len(lable):
    print("Warning: The number of predicted labels does not match the number of true labels.")
tmp = []
for p, t in zip(predicted, lable):
    #print(f"Predicted: {p}, True: {t}")
    tmp.append(p == t)

# compute MAE for score
mae = np.mean(np.abs(np.array(predicted) - np.array(lable))).item()
print(f"MAE Score: {mae}")

latency = 0
# only one line list of latency values is expected
with open(foxconn_score_timer_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        latency = np.mean(list(result)).item()

print(f"Score Latency: {latency}")

print(f"Total input tokens: {input_token_count}")
print(f"Total output tokens: {output_token_count}")
print(f"Total input cost: ${input_token_count * gpt_pricing_input:.6f}")
print(f"Total output cost: ${output_token_count * gpt_pricing_output:.6f}")
print(f"Total cost: ${input_token_count * gpt_pricing_input + output_token_count * gpt_pricing_output:.6f}")