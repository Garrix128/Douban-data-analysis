import re
from numpy import *
import pandas as ps
from . import homeData

df = ps.DataFrame(homeData.getAllData(),columns=[
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

def getRate_tType(type):
    allData = homeData.getAllData()
    rateList = []
    rateForm = {}
    for i in allData:
        for j in i[7]:
            if type == j:
                rateList.append(i[2])
    for i in rateList:
        if rateForm.get(i,-1) == -1:
            rateForm[i] = 1
        else:
            rateForm[i] = rateForm[i] + 1
    return rateForm.keys(),rateForm.values()

def getStart(movieName):
    starts = list(df.loc[df['title'].str.contains(movieName)]['star'])
    searchName = list(df.loc[df['title'].str.contains(movieName)]['title'])[0]
    startList =  [{
        'name':'五星',
        'value':0
    },{
        'name':'四星',
        'value':0
    },{
        'name': '三星',
        'value':0
    },{
        'name': '二星',
        'value':0
    },{
        'name':'一星',
        'value':0
    }]
    for i,s in enumerate(starts[0]):
        startList[i]['value'] = float(re.sub('%','',str(s)))
    return startList,searchName

def getCountryRating():
    allData = homeData.getAllData()
    data = [{
        'name':x,
        'count':0,
        'rating':[]
    } for x in ['中国','美国','英国','韩国','日本','法国','总和']]
    for i in allData:
        data[-1]['count'] = data[-1]['count'] + 1
        data[-1]['rating'].append(float(i[2]))
        for j in data:
            if i[8][0].find(j['name']) != -1:
                j['count'] = j['count'] + 1
                j['rating'].append(float(i[2]))
    x = []
    y = []
    y1 = []
    for i in data:
        i['rating'] = mean(i['rating'])
        x.append(i['name'])
        y.append(i['count'])
        y1.append(i['rating'])
    return x,y,y1

def getMean():
    def sort_fn(item):
        return item[0]
    allData = homeData.getAllData()
    meanList = {}
    for i in allData:
        if meanList.get(i[6],-1) == -1:
            meanList[i[6]] = [i[2]]
        else:
            meanList[i[6]].append(i[2])
    meanList = sorted(meanList.items(),key=sort_fn,reverse=False)
    for i,item in enumerate(meanList):
        meanList[i] = list(item)
        item = list(item)
        newList = []
        for j in range(len(item[1])):
            newList.append(float(item[1][j]))
        item.append(newList)
        item.pop(1)
        meanList[i] = item
    for i,item in enumerate(meanList):
        meanList[i][1] = mean(item[1])
    rows = []
    columns = []
    for i in meanList:
        rows.append(i[0])
        columns.append(i[1])
    return rows,columns