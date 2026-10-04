from pathlib import Path
from utils import load_config
from models.gpt import GPTClient
from dataset import FoxconnDataset
import time
import json

config = load_config("config.py")
config = load_config('./config.py')
AZURE_OPENAI_ENDPOINT = config.AZURE_ENDPOINT
AZURE_DEPLOYMENT_NAME = config.AZURE_DEPLOYMENT_NAME
AZURE_API_KEY = config.AZURE_API_KEY

gpt_client = GPTClient(endpoint=AZURE_OPENAI_ENDPOINT, api_key=AZURE_API_KEY, deployment_name=AZURE_DEPLOYMENT_NAME)
foxconn_choice = FoxconnDataset(type='choice', folder_path='dataset/starter_tasks/choice_ticket_routing.jsonl')
foxconn_noul = FoxconnDataset(type='noul', folder_path='dataset/starter_tasks/noul_release_gate.jsonl')
foxconn_score = FoxconnDataset(type='score', folder_path='dataset/starter_tasks/score_incident_priority.jsonl')

foxconn_choice_result = []
foxconn_noul_result = []
foxconn_score_result = []
foxconn_choice_timer = []
foxconn_noul_timer = []
foxconn_score_timer = []

for sample in foxconn_choice:
    t = time.time()
    result, _ = gpt_client.choice(sample)
    foxconn_choice_timer.append(time.time() - t)
    foxconn_choice_result.append(result)
    # break
for sample in foxconn_noul:
    t = time.time()
    result, _ = gpt_client.noul(sample)
    foxconn_noul_timer.append(time.time() - t)
    foxconn_noul_result.append(result)
    # break

for sample in foxconn_score:
    t = time.time()
    result, _ = gpt_client.score(sample)
    foxconn_score_timer.append(time.time() - t)
    foxconn_score_result.append(result)
    # break

avg_foxconn_choice_timer = sum(foxconn_choice_timer) / len(foxconn_choice_timer) if foxconn_choice_timer else 0
avg_foxconn_noul_timer = sum(foxconn_noul_timer) / len(foxconn_noul_timer) if foxconn_noul_timer else 0
avg_foxconn_score_timer = sum(foxconn_score_timer) / len(foxconn_score_timer) if foxconn_score_timer else 0


if not Path('./output_gpt/exp/foxconn').exists():
    Path('./output_gpt/exp/foxconn').mkdir(parents=True)

print(f'Foxxcon choice processed {len(foxconn_choice_result)} results')
print(f'Foxxcon choice average timer: {avg_foxconn_choice_timer}')
with open('./output_gpt/exp/foxconn/foxconn_choice_result.jsonl', 'w') as f:
    for item in foxconn_choice_result:
        f.write(json.dumps(item) + "\n")
with open('./output_gpt/exp/foxconn/foxconn_choice_timer.jsonl', 'w') as f:
    json.dump(foxconn_choice_timer, f)

print(f'Foxxcon noul processed {len(foxconn_noul_result)} results')
print(f'Foxxcon noul average timer: {avg_foxconn_noul_timer}')
with open('./output_gpt/exp/foxconn/foxconn_noul_result.jsonl', 'w') as f:
    for item in foxconn_noul_result:
        f.write(json.dumps(item) + "\n")
with open('./output_gpt/exp/foxconn/foxconn_noul_timer.jsonl', 'w') as f:
    json.dump(foxconn_noul_timer, f)

print(f'Foxxcon score processed {len(foxconn_score_result)} results')
print(f'Foxxcon score average timer: {avg_foxconn_score_timer}')
with open('./output_gpt/exp/foxconn/foxconn_score_result.jsonl', 'w') as f:
    for item in foxconn_score_result:
        f.write(json.dumps(item) + "\n")
with open('./output_gpt/exp/foxconn/foxconn_score_timer.jsonl', 'w') as f:
    json.dump(foxconn_score_timer, f)