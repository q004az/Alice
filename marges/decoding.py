import requests
import json
from lib.const import url
from lib.dictin import d1 as lessonType
from datetime import date
import re


def decodingMarge(event):
    text = event.get("request", {}).get("original_utterance", {}).lower()
    if 'расшифр' in text:
        pattern = r'-?\d+\.?\d*'
        number = re.findall(pattern, text)
        currentValue = json.loads(event['state']['user']['value'])
        api_url = f"{url}{currentValue['group']}/{currentValue['date']}"

        value = {
            'group': currentValue['group'],
            'date': currentValue['date']
        }
        try:
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()["lessons"]
            otvet = "Расшифрованные дисциплины:\n"
            for lesson in data:
                abbr = lesson["discipline"]["abbr"]
                disciplineTitle = lesson["discipline"]["title"]
                otvet += f"{abbr} - {disciplineTitle}\n"

            return {
                "response": {
                    "text": f"{otvet}",
                    "end_session": False
                },
                "user_state_update": {
                    "value": json.dumps(value)
                },
                "session_state": {
                    "value": 10
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
                    "value": 10
                },
                'version': '1.0'
            }
    return False