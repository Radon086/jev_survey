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
foxconn_noul = FoxconnDataset(type='noul', folder_path='dataset/starter_tasks/noul_release_gate_sp.jsonl')

foxconn_noul_result = []

for sample in foxconn_noul:
    result, _ = gpt_client.noul_sp(sample)
    foxconn_noul_result.append(result)

if not Path('./output_gpt/exp/foxconn').exists():
    Path('./output_gpt/exp/foxconn').mkdir(parents=True)

print(f'Foxxcon noul processed {len(foxconn_noul_result)} results')
with open('./output_gpt/exp/foxconn/foxconn_noul_result_sp.jsonl', 'w') as f:
    for item in foxconn_noul_result:
        f.write(json.dumps(item) + "\n")