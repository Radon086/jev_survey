import sys
from pathlib import Path
from utils import load_config
from models.jev import jevclient
from dataset import FoxconnDataset
import time

config = load_config("config.py")

jev_client = jevclient(api_key=config.JEV_API_KEY, model='jev-latest')

foxconn_choice_result = []
foxconn_noul_result = []
foxconn_score_result = []

foxconn_choice_timer = []
foxconn_noul_timer = []
foxconn_score_timer = []

foxconn_choice = FoxconnDataset(type='choice', folder_path='dataset/starter_tasks/choice_ticket_routing.jsonl')
foxconn_noul = FoxconnDataset(type='noul', folder_path='dataset/starter_tasks/noul_release_gate.jsonl')
foxconn_score = FoxconnDataset(type='score', folder_path='dataset/starter_tasks/score_incident_priority.jsonl')


print("First choice sample:")
print(foxconn_choice[0])

print("\nResult from JEV client(choice):")
t = time.time()
result = jev_client.choice(foxconn_choice[0])
print(result)
print(f"Time taken: {time.time() - t} seconds")
print('Result details:')
print(result.model)
print(result.usage)
print(str(result.usage))
print(result.answers)

'''
print('First noul sample:')
print(foxconn_noul[0])

print("\nResult from JEV client(noul):")
t = time.time()
result = jev_client.noul(foxconn_noul[0])
print(result)
print(f"Time taken: {time.time() - t} seconds")



print('First score sample:')
print(foxconn_score[0])

print("\nResult from JEV client(score):")
t = time.time()
result = jev_client.score(foxconn_score[0])
print(result)
print(f"Time taken: {time.time() - t} seconds")
'''