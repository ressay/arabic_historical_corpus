import urllib.request
from bs4 import BeautifulSoup
import basic as bs
import re

def scrape_page(parent,page,writer):
    rep = urllib.request.urlopen(parent+page)
    soup = BeautifulSoup(rep, "lxml")
    div_containers = soup.find('div',id="content")
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
    print(paragraph)
    # for node in div_container.find_all("p"):
    #     paragraph += node.text

    writer.write(str(paragraph)+ " ")
    if nextLink != "":
        scrape_page(parent,nextLink,writer)



# scrape_page(parent,"aaian-alasr-002.html",None)

def scrapeIslamic(parent,type="history"):
    rep = urllib.request.urlopen(parent)
    soup = BeautifulSoup(rep, "html.parser")
    nextLink = ""
    for node in soup.find_all("a"):
        if re.match(".*التالية.*",node.get_text()):
            nextLink = node.get("href")
    body = soup.find("tbody")

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
        era = bs.getEraFromAuthor(author)
        if era == 'unknown':
            continue

        filename = bs.getFilePath(book, era, type,author)
        # print(filename)
        writer = open(filename, encoding="utf-8", mode="w")
        # f = open("try", encoding="utf-8", mode="w")
        scrape_page(parent, link, writer)

    if nextLink != "":
        scrapeIslamic(parent+nextLink)


if __name__ == "__main__":
    parent = "http://www.islamicbook.ws/tarekh/"
    scrapeIslamic(parent)
    parents = ["http://www.islamicbook.ws/qbook/","http://www.islamicbook.ws/ageda/"
               ,"http://www.islamicbook.ws/hadeth/","http://www.islamicbook.ws/asol/",
               "http://www.islamicbook.ws/amma/"]
    for parent in parents:
        scrapeIslamic(parent,"religion")

    parent = "http://www.islamicbook.ws/adab/"
    scrapeIslamic(parent,"literature")
