from initializer import eras, eraEnd, eraStart, path

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

def getEraFromAuthor(name,lang='ar'):
    import wptools as wp
    import re
    try:
        so = wp.page(name, lang=lang).get_more()
        print(so.data['categories'])
        for st in so.data['categories']:
            if re.match("^.*(وفيات|مواليد) \d+$", st):
                date = int(re.sub("^.*(وفيات|مواليد) (\d+)$", "\g<2>", st))
                return getEraFromDate(date)
            if re.match(".*?\d+ (deaths|births)", st):
                date = int(re.sub(".*?(\d+) (deaths|births)", "\g<1>", st))
                return getEraFromDate(date)
        return "unknown"
    except LookupError:
        return "unknown"


if __name__ == "__main__":
    print(getEraFromAuthor("ابن الأثير","ar"))

