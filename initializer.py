
eras = ['Jahiliy','SadrIslam','Umayyad','Abbasid','Dual','Modern']
eraStart = [0,610,661,750,1258,1798]
eraEnd = [610,661,750,1258,1798,2019]
path = "."

def createDirectories():
    import os
    for x in eras:
        if not os.path.isdir(path + '/' + x):
            os.mkdir(path + '/' + x)  # line B
            print(x + ' created.')

def getFilePath(name,era,type='divers'):
    import os
    if era not in eras:
        return None #come on ..

    if not os.path.isdir(path + '/' + era + '/' + type):
        os.mkdir(path + '/' + era + '/' + type)
    return path + '/' + era + '/' + type + '/' + name

def getErasDict():
    return dict([(era,(start,end)) for era,start,end in zip(eras,eraStart,eraEnd)])

def getEraFromDate(date):
    for i,(start,end) in enumerate(zip(eraStart,eraEnd)):
        if start <= date < end:
            return eras[i]
    return None

if __name__ == "__main__":
    createDirectories()