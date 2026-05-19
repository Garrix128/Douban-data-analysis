from . import homeData


def getAllActorMovieNum():
    allData = homeData.getAllData()
    ActorMovieNum = {}
    for i in allData:
        for j in i[1]:
            if ActorMovieNum.get(j, -1) == -1:
                ActorMovieNum[j] = 1
            else:
                ActorMovieNum[j] = ActorMovieNum[j] + 1
    ActorMovieNum = sorted(ActorMovieNum.items(), key=lambda x: x[1])[-20:]
    x = []
    y = []
    for i in ActorMovieNum:
        x.append(i[0])
        y.append(i[1])
    return x, y


def getAllDirectorMovieNum():
    allData = homeData.getAllData()
    ActorMovieNum = {}
    for i in allData:
        for j in i[4]:
            if ActorMovieNum.get(j, -1) == -1:
                ActorMovieNum[j] = 1
            else:
                ActorMovieNum[j] = ActorMovieNum[j] + 1
    ActorMovieNum = sorted(ActorMovieNum.items(), key=lambda x: x[1])[-20:]
    x = []
    y = []
    for i in ActorMovieNum:
        x.append(i[0])
        y.append(i[1])
    return x, y
