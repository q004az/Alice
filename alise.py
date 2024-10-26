import requests
from datetime import date
import re
from lib.dictin import d1 as lessonType
from lib.const import url
from marges.today import todayMarge
from marges.tommorow import tommorowMarge
from marges.aftertommorow import aftertommorowMarge
from marges.myGroup import getGroupMarges
from marges.anyday import anydayMarge
from marges.decoding import decodingMarge
from marges.teacher import teacher

def handler(event, context):
    text1 = "Привет! Это навык 'Расписание ТУСУР'. Я могу рассказать расписание на сегодня. Просто скажи мне номер группы."

  
    MyGroupResult = getGroupMarges(event)
    if MyGroupResult:
        return MyGroupResult

    anydayResult = anydayMarge(event)
    if anydayResult:
        return anydayResult
      
    todayResult = todayMarge(event)
    if todayResult:
        return todayResult

    aftertommorowResult = aftertommorowMarge(event)
    if aftertommorowResult:
        return aftertommorowResult

    tommorowResult = tommorowMarge(event)
    if tommorowResult:
        return tommorowResult
    
    
    teacherResult = teacher(event)
    if teacherResult:
        return teacherResult

    decodingResult = decodingMarge(event)
    if decodingResult:
        return decodingResult

    return {
        "response": {
            "text": text1,
            "end_session": False
        },
        "session_state": {
            "value": 11
        },
        'version': '1.0'
    }
