from string import Template

choice_prompt = Template("""
The current state is: $state
The question is: $question
The available choices are: $choices
The answer should be provided based on the current state, available choices, and the question.
Furthermore, the answer should only be one of the available choices. Do not provide any additional information.

Answer:
""")

noul_prompt = Template("""
The current state is: $state
The question is: $question
The available choices are: True, False
The answer should be provided based on the current state, available choices, and the question.
Furthermore, the answer should only be one of the available choices. Do not provide any additional information.

Answer:
""")

noul_prompt_sp = Template("""
The current state is: $state
The question is: $question
The available choices are: True, False
The answer should be provided based on the current state, available choices, and the question.
Furthermore, the answer should only be one of the available choices and a short explanation should be provided. Do not provide any additional information.

Answer:
""")

score_prompt = Template("""
The current state is: $state
The question is: $question
The available choices are: $choices
The answer should be provided based on the current state, available choices, and the question.
Furthermore, the answer should only be one of the available choices. Ansewer must be one of the rubric numbers. Do not provide any additional information.

Answer:
""")