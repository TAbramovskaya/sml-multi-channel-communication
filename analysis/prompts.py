TAGS = [
    "технологии",
    "реклама курса",
    "акция / скидка",
    "анонс вебинара",
    "практический кейс",
    "карьерный контент",
    "обучение / гайд",
    "корпоративный опыт"
]

PASS1_SYSTEM = '''
Analyze how much the text was transformed from its original human draft.
Be precise and conservative.
Use consistent criteria across all texts.

Do NOT detect AI vs human.

Return a conservative score from 0 to 100:
0 = minimal edits
100 = heavily rewritten or reconstructed

Guidelines:
0–20 minimal edits  
21–40 light edits  
41–60 structural changes  
61–80 strong rewrite / marketing  
81–100 heavy reconstruction  

Return a JSON array with one object per input message:

[
  {
    "id": int,
    "transformation_score": int
  }
]
'''

PASS2_SYSTEM = f'''
Extract structured data.

AUTHOR:
- Extract only if explicitly stated (e.g. "с вами X", "на связи X", "меня зовут X" etc.)
- Otherwise: "admin"

TAGS:
- Select exactly 3 from this list:
{TAGS}

Return a JSON array with one object per input message:

[
  {{
    "id": int,
    "author": string,
    "tags": [string, string, string]
  }}
]
'''
