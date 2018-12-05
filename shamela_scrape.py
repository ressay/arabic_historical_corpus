import urllib.request
from bs4 import BeautifulSoup
import basic as bs
import re

def getPageText(html_page_link ,  last_page_read):
    try:
        html_page = urllib.request.urlopen(html_page_link)
    except Exception:
        return ""
    soup = BeautifulSoup(html_page, "lxml")
    page = ""
    for main_text in soup.find_all("div" , {"class" : "book-container"}):
        text = str(main_text)
        #text = re.sub("(<br\s*/?>)" , "\n" , text)
        text = re.sub("(<hr class=\"footnote\".*)|(<span.*>)|(</span>)|(<div.*>)|(</div>)", "", text)
        text = re.sub("(\n)|(\r)|(\t+)", " ", text)
        page += text
    """
    print("page after loop" + page)
    if page == last_page_read:
        print("equal")
        return ""
    else:
        print("not equal")
    """
    return page



def readBook(book_link):
    x = 1
    book = ""
    rep = urllib.request.urlopen(book_link)
    soup = BeautifulSoup(rep, "lxml")
    for main_page in soup.find_all("a"):
        read_link = main_page.get("href")
        if re.match("http://shamela.ws/browse.php/book-\d+" , read_link):
            page = ""
            while True:
                page = getPageText(read_link + "/page-" + str(x), page)
                x += 1
                if page != "":
                    book += page
                else:
                    break
            book = re.sub("(<br/>+)|(<br>)", "\n", book)
            return book
rep = urllib.request.urlopen("http://shamela.ws/index.php/categories")
soup = BeautifulSoup(rep, "lxml")

for category in soup.find_all("a"):
    category_link = category.get("href")
    if re.match("/index.php/category/\d+", category_link):
        if not re.match(".*مرقم آليا.*", category.text):
            try:
                rep = urllib.request.urlopen("http://shamela.ws" + category_link)
                soup2 = BeautifulSoup(rep, "lxml")
            except:
                pass
            for book in soup2.find_all("a"):
                book_link = book.get("href")
                if re.match("/index.php/book/\d+", book_link):
                    try:
                        author = book.parent.find("a" , {"class" : "ignore"})
                        author = author.text
                        era = bs.getEraFromAuthor(author)
                        #if not bs.bookExists(book.text, era):
                        if not bs.bookExists(book.text, era)
                            filename = bs.getFilePath(book.text, era, category.text, author)
                            b = readBook("http://shamela.ws" + book_link)
                            file = open(filename, encoding="utf-8", mode="w")
                            file.write(b)
                            file.close()
                    except:
                        pass