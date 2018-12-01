from selenium import webdriver
from time import sleep
from time import time
from bs4 import BeautifulSoup
import basic
import re


def getPageText(html_page ,  last_page_read):
    soup = BeautifulSoup(html_page, "lxml")
    page = ""
    for main_text in soup.find_all("td" , {"height" : "269"}):
        page += main_text.text
    if page == last_page_read:
        return ""

    else:
        return page


def getBookText(first_page_link):
    driver = webdriver.PhantomJS() #initialize the webdriver
    book = ""
    next_page_link = re.findall(r"page=\d" , first_page_link)
    page_number = int(re.sub("page=", "", next_page_link[0]))
    while True:
        if page_number == 1:
            driver.get(first_page_link)
            page = "first"
        else:
            next_page_link = re.sub("page=\d", "page=" + str(page_number), first_page_link)
            driver.get(next_page_link)
        page_number += 1
        sleep(1)  # wait for JS to load
        html_page = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")  # get the HTML page
        page = getPageText(html_page , page)
        if page != "":
            book += page
        else:
            break
    return book
#2244
start = time()
for x in range(1):
    link = "http://www.alwaraq.net/Core/AlwaraqSrv/bookpage?book="+str(x)+"&session=ABBBVFAGFGFHAAWER&fkey=2&page=1&option=1"
    driver = webdriver.PhantomJS()
    driver.get(link)
    sleep(1)
    rep = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup  = BeautifulSoup(rep , "lxml")
    for title in soup.find_all("title"):
        title = re.sub("  - resource for arabic books" , "" ,title.text)
    td = soup.find_all("td" , {"width" : "40%"})
    name = re.sub("(\s+تأليف :\s+)|(\s+)$" ,"" , td[1].text) + "\n"
    era = basic.getEraFromAuthor(name)
#open("titles.txt" , encoding="utf-8" , mode="w").write(names)
    filename = basic.getFilePath(title , era=era , author=name)
    open(filename , encoding="utf-8" , mode="w").write(getBookText(link))
    print(str(time() - start))
    print("done")

