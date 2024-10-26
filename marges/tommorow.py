import requests
import json
from lib.const import url
from lib.dictin import d1 as lessonType
from datetime import date, timedelta
import codecs


def tommorowMarge(event):
    currentValue = json.loads(event['state']['user']['value'])
    if 'завтра' in event.get("request", {}).get("original_utterance", {}).lower():
        format_date = date.today() + timedelta(days=1)
        current_datetime = format_date.strftime("%Y-%m-%d")
        api_url = f"{url}{currentValue['group']}/{current_datetime}"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status() 
            data = response.json()['lessons']
            disciplines = [f"{lesson['discipline']['abbr']} - {lessonType[lesson['kind']]}" for lesson in data]
            count = len([lesson['discipline']['abbr'] for lesson in data])
            value = {
            'group': currentValue['group'],
            'date': response.json()
            }
            otvet = f'Количество пар на завтра: {count}\n'
            otvet += "\n".join(disciplines)

            return {
                "response": {
                    "text": f"{otvet}\n Сказать ли вам дополнительную информмацию о парах?",
                    "end_session": False
                },
                    "user_state_update": {
                        "value": json.dumps(value, ensure_ascii=False)
                    },
                    "session_state": {
                        "value": 11
                    },
                    'version': '1.0'
            }

        except requests.exceptions.RequestException as err:
            return {
                    "response": {
                        "text": f"Произошла ошибка при получении расписания: {str(err)}.",
                        "end_session": False
                    },
                    "session_state": {
                        "value": 11
                    },
                    'version': '1.0'
            }
    return False