import sys
from pathlib import Path
from wsgiref import headers
from .decision_model import DecisionModel
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
import json
import requests
import os
from .prompt import choice_prompt, noul_prompt, noul_prompt_sp, score_prompt

class GPTClient(DecisionModel):
    def __init__(self, endpoint, api_key, deployment_name):
        super().__init__()
        self.deployment_name = deployment_name
        self.endpoint = endpoint
        self.url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version=latest&azure-beta=v1=preview"
        self.role = "you are a genral decision model, you will receive a prompt from user, and you need to porvide a reponse to given prompt."
        self.api_key = api_key
        self.headers = {
            "api-key": self.api_key ,
            "Content-Type": "application/json"
        }

    def choice(self, sample):
        super().choice(sample)

        state = sample.state
        questions = sample.questions

        responses = []
        answers = {}
        usage = {}
        latency = {}

        for q in questions:
            instruction = q.instruction
            choices = []
            for k,v in zip(q.choices.keys(), q.choices.values()):
                if v is not None:
                    choices.append(f"{k}- {v}")
                else:
                    choices.append(f"{k}")
            choices = ", ".join(choices)

            prompt = choice_prompt.substitute(state=state, choices=choices, question=instruction)
            # print(prompt)
            messages = [{"role": "system", "content": self.role}]
            messages.append({"role": "user", "content": prompt})
            payload = {
                "messages": messages,
            }
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code == 200:
                msg = response.json()['choices'][0]['message']['content']
            else:
                msg = f"Error {response.status_code}: {response.text}"
           
            answers[q.id] = msg
            responses.append(response.json())
            response_usage = response.json().get("usage", {})
            response_latency = response_usage.get("latency_checkpoint", None) 
            usage[q.id] = {
                "prompt_tokens": response_usage["prompt_tokens"],
                "completion_tokens": response_usage["completion_tokens"],
                "reasoning_tokens": response_usage["completion_tokens_details"]["reasoning_tokens"],
                "total_tokens": response_usage["total_tokens"],
            }
            latency[q.id] = response_latency["service_ttlt_ms"]

        return {'model': self.deployment_name, "answers": answers, "usage": usage, "latency": latency}, responses

    def noul(self,sample):
        super().noul(sample)
        state = sample.state
        questions = sample.questions

        responses = []
        answers = {}
        usage = {}
        latency = {}

        for q in questions:
            instruction = q.instruction
            prompt = noul_prompt.substitute(state=state, question=instruction)
            messages = [{"role": "system", "content": self.role}]
            messages.append({"role": "user", "content": prompt})
            # print(prompt)
            payload = {
                "messages": messages,
            }
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code == 200:
                msg = response.json()['choices'][0]['message']['content']
            else:
                msg = f"Error {response.status_code}: {response.text}"

            answers[q.id] = msg
            responses.append(response.json())
            response_usage = response.json().get("usage", {})
            response_latency = response_usage.get("latency_checkpoint", None) 
            usage[q.id] = {
                "prompt_tokens": response_usage["prompt_tokens"],
                "completion_tokens": response_usage["completion_tokens"],
                "reasoning_tokens": response_usage["completion_tokens_details"]["reasoning_tokens"],
                "total_tokens": response_usage["total_tokens"],
            }
            latency[q.id] = response_latency["service_ttlt_ms"]

        return {'model': self.deployment_name, "answers": answers, "usage": usage, "latency": latency}, responses
    
    def noul_sp(self,sample):
        super().noul(sample)
        state = sample.state
        questions = sample.questions

        responses = []
        answers = {}
        usage = {}
        latency = {}

        for q in questions:
            instruction = q.instruction
            prompt = noul_prompt_sp.substitute(state=state, question=instruction)
            messages = [{"role": "system", "content": self.role}]
            messages.append({"role": "user", "content": prompt})
            # print(prompt)
            payload = {
                "messages": messages,
            }
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code == 200:
                msg = response.json()['choices'][0]['message']['content']
            else:
                msg = f"Error {response.status_code}: {response.text}"

            answers[q.id] = msg
            responses.append(response.json())
            response_usage = response.json().get("usage", {})
            response_latency = response_usage.get("latency_checkpoint", None) 
            usage[q.id] = {
                "prompt_tokens": response_usage["prompt_tokens"],
                "completion_tokens": response_usage["completion_tokens"],
                "reasoning_tokens": response_usage["completion_tokens_details"]["reasoning_tokens"],
                "total_tokens": response_usage["total_tokens"],
            }
            latency[q.id] = response_latency["service_ttlt_ms"]

        return {'model': self.deployment_name, "answers": answers, "usage": usage, "latency": latency}, responses
    
    def score(self,sample):
        super().score(sample)
        state = sample.state
        questions = sample.questions

        responses = []
        answers = {}
        usage = {}
        latency = {}

        for q in questions:
            instruction = q.instruction
            rubric = []
            for r in range(len(q.rubric)):
                rubric.append(f"{r+1}: {q.rubric[r]}")
            rubric = ", ".join(rubric)

            prompt = score_prompt.substitute(state=state, choices=rubric, question=instruction)
            messages = [{"role": "system", "content": self.role}]
            messages.append({"role": "user", "content": prompt})
            #print(prompt)
            payload = {
                "messages": messages,
            }
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code == 200:
                msg = response.json()['choices'][0]['message']['content']
            else:
                msg = f"Error {response.status_code}: {response.text}"

            answers[q.id] = msg
            responses.append(response.json())
            response_usage = response.json().get("usage", {})
            response_latency = response_usage.get("latency_checkpoint", None) 
            usage[q.id] = {
                "prompt_tokens": response_usage["prompt_tokens"],
                "completion_tokens": response_usage["completion_tokens"],
                "reasoning_tokens": response_usage["completion_tokens_details"]["reasoning_tokens"],
                "total_tokens": response_usage["total_tokens"],
            }
            latency[q.id] = response_latency["service_ttlt_ms"]

        return {'model': self.deployment_name, "answers": answers, "usage": usage, "latency": latency}, responses