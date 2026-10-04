import sys
from pathlib import Path
from decision_model import DecisionModel
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
import json
import requests
import os


role = """
you are a genral decision model, you will receive a prompt from user, and you need to porvide a reponse to given prompt.
"""
AZURE_OPENAI_ENDPOINT="https://hermes-test-shoi.openai.azure.com/openai/v1"
azure_endpoint = "https://hermes-test-shoi.openai.azure.com"
deployment_name = "gpt-5.5"

url = f"{azure_endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version=latest&azure-beta=v1=preview"

def call_llm_api(prompt, history_messages=None):
    """
    使用 Azure OpenAI 進行診斷
    """

    headers = {
        "api-key": 'BHuxTAnluergGTn0AUM1eqL0envPleZZu24TKn7uiqwUKUJvfTx8JQQJ99CHACYeBjFXJ3w3AAAAACOGgTE8',
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": role}]
    messages.append({"role": "user", "content": prompt})
    print(messages)
    payload = {
        "messages": messages,
        #"temperature": 0.3 
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            msg = response.json()['choices'][0]['message']['content']
        else:
            msg = f"Error {response.status_code}: {response.text}"
        print(msg)
            
    except Exception as e:
        err_str = str(e)
        return None, None, None, err_str
    
call_llm_api("testing. say hi and adress your model name and version.")