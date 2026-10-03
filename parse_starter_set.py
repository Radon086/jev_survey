import json
import numpy as np
from collections import Counter


''' describe the metrics we will use to evaluate each task type
| Task | Primary | Secondary |
|---|---|---|
| **Choice (48)** | Accuracy | label/prediction distribution |
| **Noul (40)** | F1 + Accuracy | confusion matrix |
| **Score (40)** | MAE | Expected-score MAE / Spearman if useful |
| **All** | Latency | output validity |
'''


def get_distribution_stats(data_list):
    '''
    Get comprehensive statistics and proportions for a list
    '''
    counts = Counter(data_list)
    total = len(data_list)
    dic = {}
    summary = {}

    for value in sorted(counts.keys()):
        count = counts[value]
        proportion = count / total
        percentage = proportion * 100
        dic[value] = {
            'count': count,
            'percentage': percentage
        }

    summary['mean'] = np.mean(data_list).item()
    summary['median'] = np.median(data_list).item()
    summary['std_dev'] = np.std(data_list).item()
    summary['min'] = np.min(data_list).item()
    summary['max'] = np.max(data_list).item()

    return dic, summary


def check_choice_set(folder_path):
    '''
    Number of options per question
    - Are they all 4-way? 8 queues? Mixed?
    - This matters for the random/chance baseline.

    Ground-truth distribution across choices
    - Count A/B/C/D/etc.
    - Mainly to detect something silly like 70% of all answers being one queue.
    '''

    total_samples = 0
    choice_distribution = []
    label_distribution = []


    with open(folder_path, 'r') as f:
        for line in f:
            sample = json.loads(line)
            total_samples += 1
            chioce_types = len(sample['case_id'])
            label = sample['choices'].index(sample['label'])
            choice_distribution.append(chioce_types)
            label_distribution.append(label)
            
    
    choice_distribution_stats, choice_summary = get_distribution_stats(choice_distribution)
    label_distribution_stats, label_summary = get_distribution_stats(label_distribution)

    print(f"\nChoice distribution stats: {choice_distribution_stats}")
    print(f"Choice summary: {choice_summary}")
    print(f"Label distribution stats: {label_distribution_stats}")
    # print(f"\nLabel summary: {label_summary}") meaningless

def check_noul_set(folder_path):
    '''
    maybe just the T/F ratio
    '''
    total_samples = 0
    true_count = 0
    false_count = 0
    
    with open(folder_path, 'r') as f:
        for line in f:
            sample = json.loads(line)
            total_samples += 1
  
            if sample['label'] == True:
                true_count += 1
            elif sample['label'] == False:
                false_count += 1

    print(f"True count: {true_count} ({true_count/total_samples*100:.2f}%)")
    print(f"False count: {false_count} ({false_count/total_samples*100:.2f}%)")

def check_score_set(folder_path):
    '''
    Distribution of ground-truth scores
    '''
    label_distribution = []
    scale_values = []
    with open(folder_path, 'r') as f:
        for line in f:
            sample = json.loads(line)
            label_distribution.append(sample['label'])
            scale_max = sample['scale']['max']
            scale_values.append(scale_max)

    label_distribution_stats, label_summary = get_distribution_stats(label_distribution)
    scale_distribution_stats, scale_summary = get_distribution_stats(scale_values)

    print(f"\nLabel distribution stats: {label_distribution_stats}")
    print(f"Label summary: {label_summary}")
    print(f"Scale distribution stats: {scale_distribution_stats}")
    print(f"Scale summary: {scale_summary}")

print("Checking starter tasks datasets...")
print("\nChecking choice set...")
check_choice_set('./dataset/starter_tasks/choice_ticket_routing.jsonl')
print("\nChecking noul set...")
check_noul_set('./dataset/starter_tasks/noul_release_gate.jsonl')
print("\nChecking score set...")
check_score_set('./dataset/starter_tasks/score_incident_priority.jsonl')
