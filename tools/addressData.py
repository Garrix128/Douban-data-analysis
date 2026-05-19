from . import homeData
import pandas as ps

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


def getAddressData():
    addrsses = df['country'].values
    address = []
    for i in addrsses:
        if isinstance(i, list):
            for j in i:
                address.append(j)
        else:
            address.append(i)
    addressDic = {}
    for i in address:
        if addressDic.get(i, -1) == -1:
            addressDic[i] = 1
        else:
            addressDic[i] = addressDic[i] + 1
    return list(addressDic.keys()), list(addressDic.values())


def getLangData():
    langs = df['lang'].values
    langes = []
    for i in langs:
        if isinstance(i, list):
            for j in i:
                langes.append(j)
        else:
            langes.append(i)
    langsDic = {}
    for i in langes:
        if langsDic.get(i, -1) == -1:
            langsDic[i] = 1
        else:
            langsDic[i] = langsDic[i] + 1
    return list(langsDic.keys()), list(langsDic.values())
