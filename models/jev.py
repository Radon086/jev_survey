from .decision_model import DecisionModel
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
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
    questions: list
'''

class jevclient(DecisionModel):

    def __init__(self, api_key: str, model: str | None = None):
        self.api_key = api_key 
        self.model = model

    def choice(self, sample):
        super().choice(sample)

        state = sample.state
        questions = sample.questions
        api_questions = {q.id: Choice(instructions=q.instruction, criteria=q.choices) for q in questions}
        result = None
        
        with TypeSafeClient(api_key=self.api_key, model=self.model,) as client:
            result = client.system_one(
                state=state,
                questions=api_questions,
            )
        
        return result

    def noul(self, sample):
        super().noul(sample)
        state = sample.state
        questions = sample.questions

        result = None
        with TypeSafeClient(api_key=self.api_key, model=self.model,) as client:
            result = client.system_one(
                state=state,
                questions={q.id: Noul(instructions=q.instruction) for q in questions},
            )
        return result
    
    def score(self, sample):
        super().score(sample)

        input_state = sample.state
        questions = sample.questions
        api_questions = {q.id: Score(instructions=q.instruction, criteria=q.rubric) for q in questions}  

        result = None
        with TypeSafeClient(api_key=self.api_key, model=self.model,) as client:
            result = client.system_one(
                state=input_state,
                questions=api_questions,
            )

        return result
