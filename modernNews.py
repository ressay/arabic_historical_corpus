import urllib.request
from bs4 import BeautifulSoup
import initializer as ins

rep = urllib.request.urlopen("http://aracorpus.e3rab.com/argistestsrv.nmsu.edu/AraCorpus/Data/")
soup = BeautifulSoup(rep, "html.parser")
names = []
limit = 10
for node in soup.find_all("a"):
  if node.get("href").endswith("txt"):
    # Asr hadith, category => news
    fileName = ins.getFilePath(node.text,ins.eras[-1],"news")
    file = open(fileName, encoding="utf-8" , mode="w")
    file.write(urllib.request.urlopen("http://aracorpus.e3rab.com/argistestsrv.nmsu.edu/AraCorpus/Data/" + node.text).read().decode('windows-1256'))
    print("the file : " + node.text + "is writen succesfully")
    limit -= 1
    if not limit:
      break