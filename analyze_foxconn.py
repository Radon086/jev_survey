from pathlib import Path
from utils import load_config
from models.jev import jevclient
from dataset import FoxconnDataset
import json
import numpy as np
from sklearn.metrics import f1_score
''''
| Task | Primary metric |
|---|---|
| Choice | Accuracy |
| Noul | F1 + Accuracy |
| Score | MAE |
| All | Output validity |
'''

foxconn_choice = FoxconnDataset(type='choice', folder_path='dataset/starter_tasks/choice_ticket_routing.jsonl')
foxconn_noul = FoxconnDataset(type='noul', folder_path='dataset/starter_tasks/noul_release_gate.jsonl')
foxconn_score = FoxconnDataset(type='score', folder_path='dataset/starter_tasks/score_incident_priority.jsonl')

foxconn_choice_resulte_file = "./output/exp/foxconn/foxconn_choice_result.jsonl"
foxconn_noul_resulte_file = "./output/exp/foxconn/foxconn_noul_result.jsonl" 
foxconn_score_resulte_file = "./output/exp/foxconn/foxconn_score_result.jsonl"

##################
# choice 
##################

predicted = []
with open(foxconn_choice_resulte_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            predicted.append(answers[key]['choice'])
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
print(f"Accuracy Choice: {accuracy}")

##################
# noul
##################
predicted = []
with open(foxconn_noul_resulte_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            noul = answers[key]['noul']
            predicted.append(True if noul>=0.5 else False)
lable = []
for sample in foxconn_noul:
    questions = sample.questions
    for question in questions:
        lable.append(question.label)

if len(predicted) != len(lable):
    print("Warning: The number of predicted labels does not match the number of true labels.")
tmp = []
for p, t in zip(predicted, lable):
    #print(f"Predicted: {p}, True: {t}")
    tmp.append(p == t)

# compute accuracy for noul
accuracy = np.mean(tmp).item()
print(f"Accuracy Noul: {accuracy}")
# compute F1 score for noul
f1 = f1_score(lable, predicted)
print(f"F1 Noul: {f1}")

##################
# score
##################
predicted = []
with open(foxconn_score_resulte_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            score = answers[key]['score']
            predicted.append(score)
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