from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS()
driver.get("http://www.alwaraq.net/Core/AlwaraqSrv/bookpage?book=9&session=ABBBVFAGFGFHAAWER&fkey=2&page=1&option=1")

sleep(10)


html2 = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")


# 4 tables / 7 tr

soup = BeautifulSoup(html2, "html.parser")

file = open("try.txt" , encoding="utf-8" , mode="w")

x = 1
for main_table in soup.find_all("p"):
    file.write(main_table.text)




