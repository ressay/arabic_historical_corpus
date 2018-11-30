import urllib.request
from bs4 import BeautifulSoup
import basic
import re


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


rep = urllib.request.urlopen("https://www.aldiwan.net/")
soup = BeautifulSoup(rep, "html.parser")
i = 0;
for eras in soup.find_all("div" , {"class" : "col-md-4"}):
    for node in eras.find_all("a"):
        if node.text in ["العصر الجاهلي" , "العصر العباسي" , "العصر الإسلامي" , "العصر الأموي"] :  #   get all jahili cho3araa list link
            rep = urllib.request.urlopen("https://www.aldiwan.net/" + node.get("href"))
            soup = BeautifulSoup(rep, "html.parser")

            for node1 in soup.find_all("a" , {"class":"s-button"}):  #   get every cha3ir diwan
                rep = urllib.request.urlopen("https://www.aldiwan.net/" + node1.get("href"))
                soup2 = BeautifulSoup(rep, "html.parser")


                for node3 in soup2.find_all("a" , {"class":"pull-right"}):  #   get every chi3r from diwan link
                    #   create a file for everykassida using getFilePath function
                    exceptions = open("exceptions.txt" , encoding="utf-8" , mode="w")
                    try:
                        print("try")
                        print(i)
                        i = i+1
                        if node.text == "العصر الجاهلي":
                            filename = basic.getFilePath(node3.text, "Jahiliy", "poem", node1.text) + ".txt"
                            #error in line 40 in one of the files i get file not found (file not getting created)
                        elif node.text == "العصر العباسي":
                            filename = basic.getFilePath(node3.text, "Abbasid", "poem",node1.text) + ".txt"
                        elif node.text == "العصر الأموي":
                            filename = basic.getFilePath(node3.text, "Umayyad", "poem",node1.text) + ".txt"
                        elif node.text == "العصر الإسلامي":
                            filename = basic.getFilePath(node3.text, "SadrIslam", "poem",node1.text) + ".txt"
                        print('got name')
                        file = open(filename , encoding="utf-8" , mode="w")
                        print("file created")
                        print(filename)
                        rep = urllib.request.urlopen("https://www.aldiwan.net/" + node3.get("href"))
                        soup3 = BeautifulSoup(rep, "html.parser")
                        for main_text in soup3.find_all("div" , {"class" : "bet-1"}): #   access to kassida link and
                            chatr = 1
                            for prt in main_text.find_all("h3"):
                                if chatr % 2 == 0:
                                    file.write(prt.text)
                                else:
                                    file.write(re.sub("\n" , "\t" , prt.text))
                                chatr = chatr + 1
                            break
                        file.close()
                        print("file close")
                    except:
                        print("inside exception")
                        exceptions.write(filename)
                        file.close()