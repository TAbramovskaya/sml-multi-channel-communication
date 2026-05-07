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

INTENT = [
    "конверсия в обучение",
    "регистрация на вебинар",
    "обучающее вовлечение",
    "формирование доверия"
]

CONTENT = [
    "промо-контент",
    "практический кейс",
    "корпоративный опыт",
    "карьерный контент",
    "собеседования",
    "обучающий контент",
    "обзор индустрии",
    "студенческие кейсы",
    "интерактивный формат"
]

DELIVERY_STYLE = [
    "экспертное мнение",
    "личный опыт",
    "мотивация и поддержка",
    "информационный анонс",
    "создание срочности"
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
- Extract only if explicitly stated
  ("с вами X", "на связи X", "меня зовут X", etc.)
- Otherwise return: "Simulative"

TAG_INTENT:
Select exactly ONE from:
{INTENT}

TAG_CONTENT:
Select exactly ONE from:
{CONTENT}

TAG_DELIVERY_STYLE:
Select exactly ONE from:
{DELIVERY_STYLE}

Priority rules:
- INTENT = primary expected outcome of the message
- CONTENT = main informational substance
- DELIVERY_STYLE = dominant communication style
- If multiple categories apply, choose the category that best represents most of the message
- Ignore small promotional fragments at the end unless the entire message is promotional

Return a JSON array with one object per input message:

[
  {{
    "id": int,
    "author": string,
    "tag_intent": string,
    "tag_content": string,
    "tag_delivery_style": string
  }}
]
'''
