import requests
import json
from lib.const import url
from lib.dictin import d1 as lessonType
from datetime import date
import re, os


def decodingMarge(event):
    text = event.get("request", {}).get("original_utterance", {}).lower()
    currentValue = json.loads(event['state']['user']['value'])

    if ('расшифр' and ("все" or "всё")) in text:
        pattern = r'-?\d+\.?\d*'
        number = re.findall(pattern, text)
        
        data = currentValue['date']["lessons"]
        otvet = "Расшифрованные дисциплины:\n"
        for lesson in data:
            abbr = lesson["discipline"]["abbr"]
            disciplineTitle = lesson["discipline"]["title"]
            otvet += f"{abbr} - {disciplineTitle}\n"

        return {
                "response": {
                    "text": f"{otvet}\n Хотите узнать что нибудь еще?",
                    "end_session": False
                },
                "user_state_update": {
                    "value": event['state']['user']['value']
                },
                "session_state": {
                    "value": 11
                },
                'version': '1.0'
        }
    elif 'расшифр' in text:
        discipline = text.split()[1]
        data = currentValue['date']["lessons"]
        otvet = ''
        for lesson in data:
            if lesson["discipline"]["abbr"].lower() == discipline.lower():
            
                disciplineTitle = lesson["discipline"]["title"]
                otvet = f"{lesson['discipline']['abbr']} - {disciplineTitle}\n"
                break


        return {
            "response": {
                "text":  f"{otvet}\n Хотите узнать что нибудь еще?",
                "end_session": False
            },
            "user_state_update": {
                    "value": event['state']['user']['value']
            },
                "session_state": {
                    "value": 11
            },
            'version': '1.0'
        }

    return False




