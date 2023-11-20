from openai import OpenAI
from datetime import datetime

client = OpenAI()


def getCurrentTimeAsString():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def getAnswerFromChatGPT(user_prompt, system_prompt):
    print('request start at ' + getCurrentTimeAsString())
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    print('request end at ' + getCurrentTimeAsString())
    return completion.choices[0].message.content
