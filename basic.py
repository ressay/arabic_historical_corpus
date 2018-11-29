
from initializer import eras, eraEnd, eraStart, path

def getFilePath(name,era,type='divers',author="unknown"):
    import os
    if era not in eras:
        return None #come on ..

    if not os.path.isdir(path + '/' + era + '/' + type):
        os.mkdir(path + '/' + era + '/' + type)
    if author != "":
        name = "__"+author+"__"+name
    p = path + '/' + era + '/' + type + '/' + name
    p.replace('\t', ' ')
    p.replace('\n', ' ')
    p.replace('\r', ' ')
    return p

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
    patterns = [
        ".*Décès en.*?(\d+)",
        "^.*وفيات (\d+)$",
        ".*?(\d+) deaths",
        ".*Naissance en.*?(\d+)",
        ".*?(\d+) births",
        "^.*مواليد (\d+)$"
    ]
    try:
        so = wp.page(name, lang=lang).get_more()
        # print(so.data['categories'])
        for pattern in patterns:
            for st in so.data['categories']:
                if re.match(pattern,st):
                    date = int(re.sub(pattern,"\g<1>",st))
                    # print(st)
                    print(date)
                    return getEraFromDate(date)
            # if re.match(".*(Décès en|Naissance en)\s+\d+", st):
            #     date = int(re.sub(".*(Décès en|Naissance en)\s+(\d+)", "\g<2>", st))
            #     return getEraFromDate(date)
            # if re.match(".*?\d+ (deaths|births)", st):
            #     date = int(re.sub(".*?(\d+) (deaths|births)", "\g<1>", st))
            #     return getEraFromDate(date)
            # if re.match("^.*(وفيات|مواليد) \d+$", st):
            #     date = int(re.sub("^.*(وفيات|مواليد) (\d+)$", "\g<2>", st))
            #     return getEraFromDate(date)

        return "unknown"
    except LookupError:
        res = wikipediaFromGoogle(name)
        if res:
            lang = res[0]
            name = res[1]
        else:
            return "unknown"
        try:
            so = wp.page(name, lang=lang).get_more()
            # print(so.data['categories'])
            for st in so.data['categories']:
                for pattern in patterns:
                    if re.match(pattern, st):
                        date = int(re.sub(pattern, "\g<1>", st))
                        # print(st)
                        print(date)
                        return getEraFromDate(date)
                # if re.match("^.*(وفيات|مواليد) \d+$", st):
                #     date = int(re.sub("^.*(وفيات|مواليد) (\d+)$", "\g<2>", st))
                #     return getEraFromDate(date)
                # if re.match(".*?\d+ (deaths|births)", st):
                #     date = int(re.sub(".*?(\d+) (deaths|births)", "\g<1>", st))
                #     return getEraFromDate(date)
            return "unknown"
        except LookupError:
            return "unknown"

def wikipediaFromGoogle(query):
    import re
    from bs4 import BeautifulSoup
    import requests
    query = re.sub("\s","+",query)
    link = "https://www.google.com/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q="+query
    # r = requests.get(link)
    rep = requests.get(link)
    soup = BeautifulSoup(rep.text,"html.parser")
    first = soup.find("cite").get_text()
    result = None
    if re.match("https://.+\.wikipedia.org/wiki/.+",first):
        result = re.sub("https://(.+)\.wikipedia.org/wiki/(.+)","\g<1>*\g<2>",first).split("*")
    if not result:
        return None
    return str(result[0]),re.sub("_"," ",result[1])


def saveListOfBooks():
    import json
    books = loadListOfBooks()
    with open('books.json', 'w') as fp:
        json.dump(books, fp)

def bookExists(name,era,author='unknown',books=None):
    if not books:
        books = loadListOfBooks()
    books = books[era]
    for book in books:
        if name == book['name']:
            return True
    return False

def loadListOfBooks():
    import re
    import os
    books = {}
    for rootdir in eras:
        for folder, subs, files in os.walk(rootdir):
            if len(files):
                # print(files)
                splitted = [re.findall("__(.*)__(.*)", file)[0] for file in files]
                # print(splitted)
                books[folder] = [{"name": spl[1], "author": spl[0]} for spl in splitted]
    # print(books)
    return books





if __name__ == "__main__":
    loadListOfBooks()

    # print(getEraFromAuthor("ghandi","en"))
    # res = wikipediaFromGoogle("ghandi")
    # if res:
    #     print(res[0])
    #     print(res[1])
    #     print(getEraFromAuthor(res[1],res[0]))
