import urllib.request
from bs4 import BeautifulSoup
import basic as bs
import re


def scrape_author(soup2,cEra,author,books,setLimit,created,existed,errors):
    for node3 in soup2.find_all("a", {"class": "pull-right"}):  # get every chi3r from diwan link
        #   create a file for every kassida using getFilePath function

        if bs.bookExists(node3.text, books):
            existed = existed + 1
            print('INFO POEM EXISTED', existed, node3.text)
            setLimit -= 1
            if not setLimit:
                break
            continue
        filename = bs.getFilePath(node3.text, cEra, "شعر", author)
        if filename is None:
            errors = errors + 1
            print('ERROR POEM: filename is None', 'era is: ', str(cEra))
            continue
        try:
            file = open(filename, encoding="utf-8", mode="w")
            created = created + 1
            print('INFO POEM CREATED', created, filename)
            rep = urllib.request.urlopen("https://www.aldiwan.net/" + node3.get("href"))
            soup3 = BeautifulSoup(rep, "lxml")
            for main_text in soup3.find_all("div", {"class": "bet-1"}):  # access to kassida link and
                chatr = 1
                for prt in main_text.find_all("h3"):
                    if chatr % 2 == 0:
                        file.write(prt.text)
                    else:
                        file.write(re.sub("\n", "\t", prt.text))
                    chatr = chatr + 1
                break
            file.close()
            setLimit -= 1
            if not setLimit:
                break
        except IOError as e:
            print('ERROR POEM', e)
        if not setLimit:
            break
    return created,existed,errors,setLimit

def scrapeByAuthor(created,existed,errors):
    books = bs.loadListOfBooksByEras()
    for i in range(1,29):
        link = 'https://www.aldiwan.net/letter'+str(i)
        try:
            rep = urllib.request.urlopen(link)
            soup = BeautifulSoup(rep, "lxml")

            for node1 in soup.find_all("a", {"class": "s-button"}):  # get every cha3ir diwan
                rep = urllib.request.urlopen("https://www.aldiwan.net/" + node1.get("href"))
                soup2 = BeautifulSoup(rep, "lxml")
                author = node1.text
                era = bs.getEraFromAuthor(author)
                if era == 'unknown' or era is None:
                    continue
                c, e, er, setLimit = scrape_author(soup2, era, author,
                                                   books, 2, created, existed, errors)
                created += c
                existed += e
                errors += er
                if not setLimit:
                    break
        except Exception as e:
            print('ERROR POEM', e)
    return created,existed,errors



""" procedure :
website -> jahili -> {
                          cha3ir1 -> diwan -> {
                                              chi3r1 ,
                                              chi3r2 ,
                                              ....
                                              },
                          cha3ir2 -> diwan -> {
                                              chi3r1 ,
                                              chi3r2 ,
                                              ...
                                              }
                          ...
                          } """


def scrape_all(limit = -1):
    rep = urllib.request.urlopen("https://www.aldiwan.net/")
    soup = BeautifulSoup(rep, "lxml")
    created = 0
    existed = 0
    errors = 0
    mapEras = {
        "العصر الجاهلي" : bs.eras[0],
        'عصر المخضرمون': bs.eras[1],
        "العصر الإسلامي" : bs.eras[1],
        "العصر الاموي" : bs.eras[2],
        "العصر العباسي" : bs.eras[3],
        'العصر الايوبي' : bs.eras[4],
        'العصر العثماني' : bs.eras[4],
        'العصر المملوكي' : bs.eras[4],
        'العصر الأندلسي' : bs.eras[4]
    }

    books = bs.loadListOfBooksByEras()
    for eras in soup.find_all("div", {"class": "col-md-4"}):
        for node in eras.find_all("a"):
            if node.text in mapEras:
                setLimit = limit
                cEra = mapEras[node.text]
                if not cEra:
                    print("WARNING POEM: no era found for it", node.text)
                    continue
                try:
                    rep = urllib.request.urlopen("https://www.aldiwan.net/" + node.get("href"))
                except Exception as e:
                    print('ERROR POEM', e)
                soup = BeautifulSoup(rep, "lxml")

                for node1 in soup.find_all("a", {"class": "s-button"}):  # get every cha3ir diwan
                    rep = urllib.request.urlopen("https://www.aldiwan.net/" + node1.get("href"))
                    soup2 = BeautifulSoup(rep, "lxml")
                    c,e,er,setLimit = scrape_author(soup2,cEra,node1.text,
                                           books,setLimit,created,existed,errors)
                    created += c
                    existed += e
                    errors += er
                    if not setLimit:
                        break
    if limit == -1:
        c,e,er = scrapeByAuthor(created,existed,errors)
        created += c
        existed += e
        errors += er
    return created, existed, errors

if __name__ == '__main__':
    scrapeByAuthor(0,0,0)
    # scrape_all()
