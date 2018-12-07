import os
import xml.etree.ElementTree as ET

tree = ET.parse('quran-simple.xml')
root = tree.getroot()

def _createXml(name,ayat,type,savePath,id):
    root = ET.Element("root",encoding='utf-8')
    metaData = ET.SubElement(root,'metadata')
    ET.SubElement(metaData, 'book_name').text = name
    ET.SubElement(metaData, 'era').text = "all"
    auth = ET.SubElement(metaData, 'author')
    ET.SubElement(auth, 'name').text = "/"
    ET.SubElement(auth, 'birth').text = "/"
    ET.SubElement(auth, 'death').text = "/"
    ET.SubElement(metaData, 'type').text = type
    ET.SubElement(metaData, 'id').text = str(id)
    sentences = ayat
    ET.SubElement(metaData, 'size').text = str(len(sentences))
    doc = ET.SubElement(root, "doc")
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


def build(idStart,xmlDir):
    surat = get_surat()
    for sura in surat:
        print(surat[sura])
        _createXml(sura, surat[sura], "quran", xmlDir+"/quran",idStart)
        idStart += 1
    return idStart
