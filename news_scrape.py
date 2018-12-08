import urllib.request
from bs4 import BeautifulSoup
import basic as bs

def scrape_all(limit=-1):
  rep = urllib.request.urlopen("http://aracorpus.e3rab.com/argistestsrv.nmsu.edu/AraCorpus/Data/")
  soup = BeautifulSoup(rep, "html.parser")
  names = []
  books = bs.loadListOfBooksByEras()
  created = 0
  existed = 0
  errors = 0

  for node in soup.find_all("a"):
    if node.get("href").endswith("txt"):
      # Asr hadith, category => news
      if bs.bookExists(node.text,books):
          existed = existed + 1
          print('INFO NEWS EXISTED', existed, node.text)
          continue
      fileName = bs.getFilePath(node.text, bs.eras[-1], "أخبار")

      file = open(fileName, encoding="utf-8", mode="w")
      if fileName is None:
        errors = errors + 1
        print('ERROR NEWS', errors, ': filename is None')
        continue
      file.write(urllib.request.urlopen(
        "http://aracorpus.e3rab.com/argistestsrv.nmsu.edu/AraCorpus/Data/" + node.text).read().decode('windows-1256'))

      created = created + 1
      print('INFO NEWS CREATED', created, node.text)
      limit -= 1
      if not limit:
        break
  return created, existed, errors
  

if __name__ == '__main__':
    scrape_all()