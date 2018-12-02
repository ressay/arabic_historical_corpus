import nltk
import re
import os
import xml.etree.ElementTree as ET
import pprint

tree = ET.parse('quran-simple.xml')
root = tree.getroot()

def _createXml(name,ayat,type,savePath,era):
    root = ET.Element("root",encoding='utf-8')
    metaData = ET.SubElement(root,'metadata')
    ET.SubElement(metaData, 'book_name').text = name
    ET.SubElement(metaData, 'era').text = era
    auth = ET.SubElement(metaData, 'author')
    ET.SubElement(auth, 'name').text = None
    ET.SubElement(auth, 'birth').text = None
    ET.SubElement(auth, 'death').text = None
    ET.SubElement(metaData, 'type').text = type
    doc = ET.SubElement(root, "doc")
    sentences = ayat
    for sentence in sentences:
        ET.SubElement(doc, "sentence").text = sentence
    tree = ET.ElementTree(root)
    savePath = savePath
    if not os.path.isdir(savePath):
        os.makedirs(savePath)
    filepath = savePath+'/'+name+".xml"
    tree.write(filepath)
    return filepath


def get_surat():
    surat={}
    tree = ET.parse('quran-simple.xml')
    root = tree.getroot()

    for child in root.iter('sura'):
        # print(child.attrib['name'])
        surat[child.attrib['name']]=[]
        for gch in child.iter('aya'):
            surat[child.attrib['name']].append(gch.attrib['text'])
    return surat


surat = get_surat()
for sura in surat:
    print(surat[sura])
    _createXml(sura,surat[sura],"book","quraan","SadrIslam")
