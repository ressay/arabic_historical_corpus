import urllib.request
from bs4 import BeautifulSoup
import basic as bs

def scrape_page(parent,page,writer):
    rep = urllib.request.urlopen(parent+page)
    soup = BeautifulSoup(rep, "html.parser")
    div_containers = soup.find_all('div')
    for div in div_containers:
        paragraph = div.text
        print(paragraph)
    # for node in div_container.find_all("p"):
    #     paragraph += node.text
    # f = open("try", encoding="utf-8", mode="w")
    # f.write(str(paragraph))

parent = "http://www.islamicbook.ws/tarekh/"
rep = urllib.request.urlopen(parent)
soup = BeautifulSoup(rep, "html.parser")
body = soup.find("tbody")

for tr in body.find_all("tr"):
    i = 0
    link = ""
    author = ""
    book = ""
    for i,td in enumerate(tr.find_all("td")):
        if not i:
            continue
        if i == 1:
            link = td.find("a").get("href")
        if i == 2:
            author = td.text
        if i == 3:
            book = td.text
    era = bs.getEraFromAuthor(author)
    if era == 'unknown':
        continue
    type = "history"
    filename = bs.getFilePath(book,era,type)
    writer = open(filename, encoding="utf-8", mode="w")
    scrape_page(parent,link,writer)
    break