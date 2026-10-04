from models.gpt import GPTClient
from dataset import FoxconnDataset
from utils import load_config


config = load_config('./config.py')
AZURE_OPENAI_ENDPOINT = config.AZURE_ENDPOINT
AZURE_DEPLOYMENT_NAME = config.AZURE_DEPLOYMENT_NAME
AZURE_API_KEY = config.AZURE_API_KEY

gpt_client = GPTClient(endpoint=AZURE_OPENAI_ENDPOINT, api_key=AZURE_API_KEY, deployment_name=AZURE_DEPLOYMENT_NAME)
foxconn_choice = FoxconnDataset(type='choice', folder_path='dataset/starter_tasks/choice_ticket_routing.jsonl')
foxconn_noul = FoxconnDataset(type='noul', folder_path='dataset/starter_tasks/noul_release_gate.jsonl')
foxconn_score = FoxconnDataset(type='score', folder_path='dataset/starter_tasks/score_incident_priority.jsonl')


print("Testing choice model:")
results, _ = gpt_client.choice(foxconn_choice[0])
print(results)

print("\nTesting noul model:")
results, _ = gpt_client.noul(foxconn_noul[0])
print(results)


print("\nTesting score model:")
results, _ = gpt_client.score(foxconn_score[0])
print(results)
