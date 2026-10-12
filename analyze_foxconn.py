from dataset import FoxconnDataset
import json
import numpy as np
from sklearn.metrics import f1_score
import os

'''
| Task | Primary metric |
|---|---|
| Choice | Accuracy |
| Noul | F1 + Accuracy |
| Score | MAE |
| All | Output validity |
'''


# Function to sort score results by absolute error value form largest to smallest
def sort_socre_reult_by_absolute_value(wrong_predictions):
    return sorted(wrong_predictions, key=lambda x: x['absolute_error'] if 'absolute_error' in x else 0, reverse=True)


jev_pricing_input = 0.042/1000000 # 0.042 dollars per 1 million tokens 
jev_pricing_output = 0/1000000 # 0 dollars per 1 million tokens

foxconn_choice = FoxconnDataset(type='choice', folder_path='dataset/starter_tasks/choice_ticket_routing.jsonl')
foxconn_noul = FoxconnDataset(type='noul', folder_path='dataset/starter_tasks/noul_release_gate.jsonl')
foxconn_score = FoxconnDataset(type='score', folder_path='dataset/starter_tasks/score_incident_priority.jsonl')

foxconn_choice_result_file = "./output/exp/foxconn/foxconn_choice_result.jsonl"
foxconn_choice_timer_file = "./output/exp/foxconn/foxconn_choice_timer.jsonl"
foxconn_noul_result_file = "./output/exp/foxconn/foxconn_noul_result.jsonl" 
foxconn_noul_timer_file = "./output/exp/foxconn/foxconn_noul_timer.jsonl"
foxconn_score_result_file = "./output/exp/foxconn/foxconn_score_result.jsonl"
foxconn_score_timer_file = "./output/exp/foxconn/foxconn_score_timer.jsonl"

input_token_count = 0
output_token_count = 0

print("Starting analysis for Foxconn dataset on Jev 1.13.0 output...")

##################
# choice 
##################

predicted = []
with open(foxconn_choice_result_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            predicted.append(answers[key]['choice'])
        usage = result['usage']
        input_token_count+=usage['input_tokens']
        output_token_count+=usage['output_tokens']

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

latency = 0
# only one line list of latency values is expected
with open(foxconn_choice_timer_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        latency = np.mean(list(result)).item()

print(f"Choice Latency: {latency}")

##################
# noul
##################
predicted = []
predicted_confidence = [] 
with open(foxconn_noul_result_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            noul = answers[key]['noul']
            predicted.append(True if noul>=0.5 else False)
            predicted_confidence.append({
                "case_index": key,
                "confidence": noul
            })
        usage = result['usage']
        input_token_count+=usage['input_tokens']
        output_token_count+=usage['output_tokens']
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

# list the wrong predictions for noul, and trivial infos such as state, predicted labels, the confidence scores, and the ground truth labels
wrong_predictions = []
for i, (p, t) in enumerate(zip(predicted, lable)):
    if p != t:
        wrong_predictions.append({
            "index": predicted_confidence[i]["case_index"] if i < len(predicted_confidence) else None,
            "state": foxconn_noul[i].state if hasattr(foxconn_noul[i], 'state') else None,
            "predicted": p,
            "confidence": predicted_confidence[i]["confidence"] if i < len(predicted_confidence) else None,
            "ground_truth": t,
        })

if not os.path.exists("./output/exp/foxconn/error_report/"):
    os.makedirs("./output/exp/foxconn/error_report/")

with open("./output/exp/foxconn/error_report/wrong_predictions_noul.jsonl", "w") as f:
    for item in wrong_predictions:
        f.write(json.dumps(item) + "\n")

#print(f"Wrong Predictions Noul: {wrong_predictions}")
#print(wrong_predictions)

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
predicted_confidence_probability = []
with open(foxconn_score_result_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        answers = result['answers']
        for key in answers.keys():
            score = answers[key]['score']
            # jev score need to shift labels by one
            shifted_score = score + 1
            predicted.append(shifted_score)
            shiftted_probability ={}
            shiftted_probability[1] = answers[key]['probabilities']['0']
            shiftted_probability[2] = answers[key]['probabilities']['1']
            shiftted_probability[3] = answers[key]['probabilities']['2']
            shiftted_probability[4] = answers[key]['probabilities']['3']
            shiftted_probability[5] = answers[key]['probabilities']['4']
            predicted_confidence_probability.append({
                "case_index": key,
                "confidence": answers[key]['confidence'],
                "probability": shiftted_probability,
            })
        usage = result['usage']
        input_token_count+=usage['input_tokens']
        output_token_count+=usage['output_tokens']
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

# list the wrong predictions for score, list the state, predicted labels, the confidence scores, and the ground truth labels
wrong_predictions = []
for i, (p, t) in enumerate(zip(predicted, lable)):
    if p != t:
        wrong_predictions.append({
            "index": predicted_confidence_probability[i]["case_index"] if i < len(predicted_confidence_probability) else None,
            "state": foxconn_score[i].state if hasattr(foxconn_score[i], 'state') else None,
            "question": foxconn_score[i].questions[0].instruction if hasattr(foxconn_score[i].questions[0], 'instruction') else None,
            "predicted": p,
            "confidence": predicted_confidence_probability[i] if i < len(predicted_confidence_probability) else None,
            "ground_truth": t,
            "absolute_error": abs(p - t)
        })

with open("./output/exp/foxconn/error_report/wrong_predictions_score.jsonl", "w") as f:
    for item in wrong_predictions:
        f.write(json.dumps(item) + "\n")

sorted_wrong_predictions = sort_socre_reult_by_absolute_value(wrong_predictions)
with open("./output/exp/foxconn/error_report/wrong_predictions_score_sorted.jsonl", "w") as f:
    for item in sorted_wrong_predictions:
        f.write(json.dumps(item) + "\n")

latency = 0
# only one line list of latency values is expected
with open(foxconn_score_timer_file, 'r') as f:
    for line in f:
        result = json.loads(line)
        latency = np.mean(list(result)).item()

print(f"Score Latency: {latency}")

print(f"Total input tokens: {input_token_count}")
print(f"Total output tokens: {output_token_count}")
print(f"Total input cost: ${input_token_count * jev_pricing_input:.6f}")
print(f"Total output cost: ${output_token_count * jev_pricing_output:.6f}")
print(f"Total cost: ${input_token_count * jev_pricing_input + output_token_count * jev_pricing_output:.6f}")