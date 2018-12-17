import urllib.request
from bs4 import BeautifulSoup
import basic as bs

created = 0
existed = 0
errors = 0
n = 0


def scrape_page(parent, page, writer):
    rep = urllib.request.urlopen(parent + page)
    soup = BeautifulSoup(rep, "lxml")
    div_containers = soup.find('div', id="content")
    div_containers.find("h1").extract()
    node = div_containers.find("h6")
    if node:
        node.extract()
    # for div in div_containers:
    nextLink = ""
    nex = False
    for node in div_containers.find_all("a"):
        if nex:
            nex = False
            nextLink = node.get("href")
        if node.get("href") == page:
            nex = True
        node.extract()
    for br in div_containers.find_all("br"):
        br.replace_with("\n")
    paragraph = div_containers.get_text()
    # print(paragraph)
    # for node in div_container.find_all("p"):
    #     paragraph += node.text

    writer.write(str(paragraph) + " ")
    if nextLink != "":
        scrape_page(parent, nextLink, writer)


def scrapeIslamic(parent, page, type="تاريخ", limit=-1):
    global created, existed, errors
    rep = urllib.request.urlopen(parent + page)
    soup = BeautifulSoup(rep, "html.parser")
    nextLink = ""
    for node in soup.find_all("a"):
        if "التالية" in node.get_text():
            nextLink = node.get("href")
    body = soup.find("tbody")
    books = bs.loadListOfBooksByEras()
    for tr in body.find_all("tr"):
        i = 0
        link = ""
        author = ""
        book = ""
        con = False
        for i, td in enumerate(tr.find_all("td")):
            if not i:
                continue
            if i == 1:
                n = td.find("a")
                if n:
                    link = n.get("href")
                else:
                    con = True
                    break
            if i == 2:
                author = td.text
            if i == 3:
                book = td.text
        if con: continue


        if bs.bookExists(book, books):
            existed = existed + 1
            print('INFO ISLAMIC_BOOK EXISTED', existed, book)
            limit -= 1
            if not limit:
                return
            continue

        era = bs.getEraFromAuthor(author)

        if era == 'unknown':
            continue

        filename = bs.getFilePath(book, era, type, author)
        if filename is None:
            errors = errors + 1
            print('ERROR ISLAMIC_BOOK', errors, ': filename is None', 'era is: ', str(era))
            continue
        writer = open(filename, encoding="utf-8", mode="w")
        created = created + 1
        print('INFO ISLAMIC_BOOK CREATED', created, filename)
        limit -= 1
        if not limit:
            return
        # f = open("try", encoding="utf-8", mode="w")
        scrape_page(parent, link, writer)
        writer.close()

    if nextLink != "":
        scrapeIslamic(parent, nextLink, type)


def scrape_all(limit=-1):
    parent = "http://www.islamicbook.ws/tarekh/"
    scrapeIslamic(parent, "", limit=limit)

    parents = ["http://www.islamicbook.ws/qbook/", "http://www.islamicbook.ws/ageda/"
        , "http://www.islamicbook.ws/hadeth/", "http://www.islamicbook.ws/asol/", ]
    for parent in parents:
        scrapeIslamic(parent, "", "دين", limit=limit)
        if limit > 0:  # light mode selected
            break

    parent = "http://www.islamicbook.ws/adab/"
    scrapeIslamic(parent, "", "أدب", limit=limit)

    parent = "http://www.islamicbook.ws/amma/"
    scrapeIslamic(parent, "", "متنوعة", limit=limit)

    return created, existed, errors


if __name__ == "__main__":
    scrape_all()
