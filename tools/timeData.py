from . import homeData
import pandas as ps
from datetime import datetime

df = ps.DataFrame(homeData.getAllData(), columns=[
    'id',
    'directors',
    'rate',
    'title',
    'casts',
    'cover',
    'year',
    'types',
    'country',
    'lang',
    'time',
    'movieTime',
    'commentLen',
    'star',
    'summary',
    'imgList',
    'detailLink'
])


def getTimeList():
    timeList = list(df['time'])
    defaultDate = '2025-01-01'
    for i, date_str in enumerate(timeList):
        try:
            timeList = [date for date in timeList if date is not None]
            timeList.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
        except (ValueError, TypeError):
            timeList[i] = defaultDate
    timeData = {}
    for i in timeList:
        if timeData.get(i[0:4], -1) == -1:
            timeData[i[0:4]] = 1
        else:
            timeData[i[0:4]] = timeData[i[0:4]] + 1
    return timeData.keys(), timeData.values()


def getMovieTimeList():
    moveiTime = list(df['movieTime'])
    moveTimeDate = [{
        'name': '短',
        'value': 0
    }, {
        'name': '中',
        'value': 0
    }, {
        'name': '长',
        'value': 0
    }, {
        'name': '特长',
        'value': 0
    }]
    for i in moveiTime:
        if int(i) <= 80:
            moveTimeDate[0]['value'] = moveTimeDate[0]['value'] + 1
        elif int(i) <= 120:
            moveTimeDate[1]['value'] = moveTimeDate[1]['value'] + 1
        elif int(i) <= 150:
            moveTimeDate[2]['value'] = moveTimeDate[2]['value'] + 1
        else:
            moveTimeDate[3]['value'] = moveTimeDate[3]['value'] + 1
    return moveTimeDate
