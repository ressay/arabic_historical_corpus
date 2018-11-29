import xml.etree.cElementTree as ET

from HistoricalCorpus import HistoricalCorpus


def createXml():
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")

    ET.SubElement(doc, "field1", name="blah").text = "some value1"
    ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

    tree = ET.ElementTree(root)
    tree.write("filename.xml")

def readXml():
    import nltk
    corpus = HistoricalCorpus('xmlCorpus','.*')
    print(corpus.sents())
readXml()