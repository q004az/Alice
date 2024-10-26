import requests
import json
from lib.const import url
from lib.dictin import d1 as lessonType
from datetime import date
import re

def teacher(event):
    text = event.get("request", {}).get("original_utterance", {}).lower()
    currentValue = json.loads(event['state']['user']['value'])
    if "препод" in text:
        otvet = ""
        data = currentValue['date']['lessons']
        for lesson in data:
            abbr = lesson["discipline"]["abbr"]
            for lecturer in lesson["lecturers"]:
                teacher_lastname = lecturer["lastname"]
                teacher_firstname = lecturer["firstname"]
                teacher_middlename = lecturer["middlename"]
                otvet += f"{abbr} - {teacher_lastname} {teacher_firstname} {teacher_middlename}\n"
        
        return {
                "response": {
                    "text": f"{otvet}\n Хотите узнать что-нибудь еще?",
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