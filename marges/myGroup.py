import requests
import re
import json
from lib.const import url
from datetime import date

def getGroupMarges(event):
    #тут надо будет добавить все возможные варианты записи групп
    formats_group = [
        r"\d{3}-\d{1}",           
    ]
    text = event.get("request", {}).get("original_utterance", {}).lower()
    # if any(re.match(format_group, event["request"]["original_utterance"]) for format_group in formats_group):
    for format_group in formats_group:
        if re.search(format_group, text):
            group_number = re.search(format_group, text).group(0)
            api_url = f"{url}{group_number}"
            value = {
                'group':group_number,
                'date':''
            }
            try:
                response = requests.get(api_url)
                response.raise_for_status() 
                
                return {
                        "response": {
                            "text": "Хорошо, я запомнила вашу группу. На какой день вы хотите узнать расписание?",
                            "end_session": False
                        },
                        "user_state_update": {
                            "value": json.dumps(value)
                        },
                        "session_state": {
                            "value": 11
                        },
                        'version': '1.0'
                    }
            except requests.exceptions.RequestException as err:
                return {
                    "response": {
                        "text": "Такой группы не существует",
                        "end_session": False
                    },
                    "session_state": {
                        "value": 11
                    },
                    'version': '1.0'
                }
    return False