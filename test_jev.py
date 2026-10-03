import sys
from pathlib import Path
from utils import load_config
from models.jev import jevclient
from dataset import FoxconnDataset

config = load_config("config.py")

jev_client = jevclient(api_key=config.JEV_API_KEY, model='jev-latest')

foxccon_choice = FoxconnDataset(type='choice', folder_path='dataset/starter_tasks/choice_ticket_routing.jsonl')
foxccon_noul = FoxconnDataset(type='noul', folder_path='data/starter_tasks/noul_release_gate.jsonl')
foxccon_score = FoxconnDataset(type='score', folder_path='data/starter_tasks/score_incident_priority.jsonl')