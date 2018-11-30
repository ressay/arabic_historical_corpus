import sys
import getopt

eras = ['Jahiliy','SadrIslam','Umayyad','Abbasid','Dual','Modern']
eraStart = [0,610,661,750,1258,1798]
eraEnd = [610,661,750,1258,1798,2019]
path = "./rawData" # where to put scraped files

def createDirectories():
    import os
    for x in eras:
        if not os.path.isdir(path + '/' + x):
            os.makedirs(path + '/' + x)  # line B
            print(x + ' created.')

if __name__ == "__main__":
    import islamicbook_scrape
    import news_scrape
    import chi3r_scrape
    import cleaner
    import os

    createDirectories()
    light_scrape = True
    xmlDir = 'tryXmlCorpus'  # where to put xml files
    options, remainder = getopt.getopt(sys.argv[1:], 'l',[])
    for opt,arg in options:
        if opt == '-l':
            print('light scraping mode selected')
            light_scrape = True
        else:
            print('heavy scrape mode selected')
            exit(1)


    if light_scrape:
        islamicbook_scrape.scrape_all(3)
        # news_scrape.scrape_all(1)
        chi3r_scrape.scrape_all(20)
    else:
        islamicbook_scrape.scrape_all()
        news_scrape.scrape_all()
        chi3r_scrape.scrape_all()

    # cleaning
    cleaner.clean()

    # convert to xml
    if not os.path.isdir(xmlDir):
        os.makedirs(xmlDir)  # line B
    cleaner.convertScrapedToXml(xmlDir)