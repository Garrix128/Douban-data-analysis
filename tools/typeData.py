from . import homeData
import pandas as ps
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

def getMovieTypeData():
    types = df['types'].values
    type = []
    for i in types:
        if isinstance(i,list):
             for j in i:
                type.append(j)
        else:
                type.append(i)
    typeDic = {}
    for i in type:
        if typeDic.get(i,-1) == -1:
            typeDic[i] = 1
        else:
            typeDic[i] = typeDic[i] + 1
    result = []
    for key,value in typeDic.items():
        result.append({
            'name':key,
            'value':value
        })
    return result

