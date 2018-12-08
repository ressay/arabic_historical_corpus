import os
import xml.etree.cElementTree as ET

import nltk

import basic as bs
import initializer
from Corpus.HistoricalCorpus import HistoricalCorpus
import quran_corpus_builder

def clean():
    _cleanNotFound()
    _moveAstrayBooks([])

def _cleanNotFound():
    bookByEras = bs.loadListOfBooksByEras()
    for era in bookByEras:
        books = bookByEras[era]
        for book in books:
            notFound = False
            with open(book['path'],'r') as f:
                empty = True
                for line in f:
                    if len(line) > 0:
                        empty = False
                    if 'sorry' in line.lower():
                        # print(line)
                        notFound = True
            if notFound or empty:
                os.remove(book['path'])
def _normalize_text(content):
    import pyarabic.araby as ar
    content = ar.strip_tatweel(content)
    content = ar.strip_tashkeel(content)
    content = ar.normalize_ligature(content)
    return content

def _clean_text(content):
    content = _normalize_text(content)
    return content

def _moveAstrayBooks(booksToMove):
    pass

def _createXml(path,name,author,type,savePath,era,id):
    import re
    root = ET.Element("root",encoding='utf-8')
    metaData = ET.SubElement(root,'metadata')
    ET.SubElement(metaData, 'book_name').text = name
    ET.SubElement(metaData, 'era').text = era
    auth = ET.SubElement(metaData, 'author')
    ET.SubElement(auth, 'name').text = author['name']
    ET.SubElement(auth, 'birth').text = str(author['birth'])
    ET.SubElement(auth, 'death').text = str(author['death'])
    ET.SubElement(metaData,'id').text = str(id)
    ET.SubElement(metaData, 'type').text = type

    content = open(path,'r').read()
    content = _clean_text(content)
    sentences = _sentenceTokenizer(content)
    # print(str(len(sentences)))
    ET.SubElement(metaData, 'size').text = str(len(sentences))
    doc = ET.SubElement(root, "doc")
    for sentence in sentences:
        if len(re.sub("\s","",sentence)) > 0:
            ET.SubElement(doc, "sentence").text = sentence
    tree = ET.ElementTree(root)
    savePath = savePath+'/'+type
    if not os.path.isdir(savePath):
        os.mkdir(savePath)
    filepath = savePath+'/'+name+".xml"
    tree.write(filepath)
    return filepath

def containsPunctuation(content):
    if '.' in content:
        return True
    return False
def _sentenceTokenizer(content):
    if not containsPunctuation(content):
        return content.splitlines() #if it doesn't contains punctuation we split by line
    sentences = nltk.PunktSentenceTokenizer().tokenize(content)
    return sentences

def convertScrapedToXml(xmlDir='xmlCorpus', id_start=1):
    print('INFO XML CONVERTER: assining ids from', id_start)
    books = bs.loadListOfBooksByEras()
    import json
    id = id_start
    tempAuthors = {}

    for era in bs.eras:
        dir = xmlDir + '/' + era
        if not os.path.isdir(dir):
            os.mkdir(dir)
        limit = -1
        for book in books[era]:
            print('INFO CLEAN: cleaning book:', book['name'])
            if book['author'] in tempAuthors:
                infos = tempAuthors[book['author']]
            else:
                try:
                    infos = bs.getBirthDeathFromAuthor(book['author'])
                    tempAuthors[book['author']] = infos
                except Exception as e:
                    print('ERROR CLEAN', e)
                    continue

            author = {'name': book['author'], 'birth': infos[0], 'death': infos[1]}
            path = _createXml(book['path'], book['name'], author, book['type'], dir,era,id)
            id += 1
            limit-=1
            if not limit: break
    corpus = HistoricalCorpus(xmlDir)
    bk = corpus.booksDescription()
    print('INFO CLEAN: creating book_description.json')
    with open(xmlDir+'/books_description.json', 'w') as fp:
        json.dump(bk, fp)

    return id_start

def _readXml():
    corpus = HistoricalCorpus(initializer.xmlDir)
    print('INFO CLEAN: len(fileids):', len(corpus.fileids()))
    tagged_words = corpus.lemma_words(end=10)
    tagged_words = corpus.lemma_words(end=200)
    sents = corpus.lemma_sents(end=20)
    stop = set(nltk.corpus.stopwords.words("arabic"))
    print('INFO CLEAN: stopwords:', stop)
    import json
    words = json.loads(open("wassit.json").read())
    words = set([w.replace(' ','') for w in words.keys()])
    print('INFO CLEAN: wassit contains', len(words), 'words')
    # print(words)
    apps = corpus.words_apparitions(words,stop_words=stop)
    with open('apps2.json', 'w') as fp:
        json.dump(apps, fp)



if __name__ == '__main__':
    # convertScrapedToXml()
    _readXml()