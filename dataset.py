from dataclasses import dataclass
import json

'''
choice input format:
{
  "new_choice_1": {
    "type": "choice",
    "instructions": "Which option best fits the state?",
    "criteria": {
      "option_a": "Description of an option",
      "option_b": "Another description of a distinct option",
      "option_c": "Another mutually exclusive option"
    }
  }
}
noul input format:

{
  "new_noul_1": {
    "type": "noul",
    "instructions": "Ask a yes or no question",
    "criteria": {
      "true": "",
      "false": ""
    }
  }
}

{
  "new_score_1": {
    "type": "score",
    "instructions": "Where does the state fall on the scale?",
    "criteria": [
      "Lowest level of one dimension",
      "Middle level of the same dimension",
      "Highest level of the same dimension"
    ]
  }
}

'''

@dataclass
class DecisionQuestion:
    id: str
    type: str
    instruction: str
    choices: dict[str, str] | None = None
    rubric: list[str] | None = None
    label: int | bool | str | None = None

@dataclass
class DecisionSample:
    id: str
    state: str
    questions: list[DecisionQuestion]

class FoxconnDataset:
    
    def __init__(self, type: str, folder_path: str):
        self.type = type
        self.samples = []
        if type == 'choice':
            self.load_choice_samples(folder_path)
        elif type == 'noul':
            self.load_noul_samples(folder_path)
        elif type == 'score':
            self.load_score_samples(folder_path)
        else:
            raise ValueError(f"Unknown dataset type: {type}")
        
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

    def load_choice_samples(self, folder_path: str):
        # Load choice samples from the specified folder
        with open(folder_path, 'r') as f:
            for line in f:
                input_state =''
                input_questions = []

                sample = json.loads(line)
                case_id = sample['case_id']
                label = sample['label']
                choices = sample['choices']
                state = sample['state']
                question = sample['question']

                decision_question = DecisionQuestion(
                    id=f"{case_id}_1",
                    type='choice',
                    instruction=question,
                    choices={f"{choice}": None for choice in choices},
                    label=label
                )

                input_state = state
                input_questions.append(decision_question)

                self.samples.append(DecisionSample(
                    id=case_id,
                    state=input_state,
                    questions=input_questions,
                ))

    def load_noul_samples(self, folder_path: str):
        # Load noul samples from the specified folder
        with open(folder_path, 'r') as f:
            for line in f:
                input_state =''
                input_questions = []

                sample = json.loads(line)
                case_id = sample['case_id']
                label = sample['label']
                state = sample['state']
                question = sample['question']

                input_state = state
                decision_question = DecisionQuestion(
                    id=f"{case_id}_1",
                    type='noul',
                    instruction=question,
                    label=label
                )
                input_questions.append(decision_question)

                self.samples.append(DecisionSample(
                    id=case_id,
                    state=input_state,
                    questions=input_questions,
                ))
    
    def load_score_samples(self, folder_path: str):
        # Load score samples from the specified folder
        with open(folder_path, 'r') as f:
            for line in f:
                input_state =''
                input_questions = []

                sample = json.loads(line)
                case_id = sample['case_id']
                label = sample['label']
                state = sample['state']
                question = sample['question']

                input_state = state
                decision_question = DecisionQuestion(
                    id=f"{case_id}_1",
                    type='score',
                    instruction=question,
                    rubric=[
                        "informational",
                        "low operational impact",
                        "moderate operational impact",
                        "high operational impact",
                        "critical / immediate response",
                    ],
                    label=label
                )
                input_questions.append(decision_question)

                self.samples.append(DecisionSample(
                    id=case_id,
                    state=input_state,
                    questions=input_questions,
                ))