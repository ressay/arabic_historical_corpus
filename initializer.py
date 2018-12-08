import sys
import getopt
from pathlib import Path
home = str(Path.home())
import tempfile

eras = ['Jahiliy','SadrIslam','Umayyad','Abbasid','Dual','Modern']
mapEraToArabic = {
    eras[0]: 'العصر الجاهلي',
    eras[1]: 'عصر صدر الإسلام',
    eras[2]: 'عصر بني أمية',
    eras[3]: 'عصر بني العباس',
    eras[4]: 'عصر الدول المتتابعة',
    eras[5]: 'العصر الحديث'
}
eraStart = [460,610,661,750,1258,1798]
eraEnd = [610,661,750,1258,1798,2019]
path = str(Path.home())+"/rawData" # where to put scraped files
xmlDir = str(Path.home())+'/xmlCorpus'  # where to put xml files
def createDirectories():
    import os
    for x in eras:
        if not os.path.isdir(path + '/' + x):
            os.makedirs(path + '/' + x)  # line B
            print('INFO INIT:', x + ' created.')

if __name__ == "__main__":
    import islamicbook_scrape
    import news_scrape
    import chi3r_scrape
    import shamela_scrape
    import cleaner
    import os


    print ('INFO INIT: initializer started')

    createDirectories()
    light_scrape = False

    options, remainder = getopt.getopt(sys.argv[1:], 'l',[])
    for opt,arg in options:
        if opt == '-l':
            light_scrape = True


    print('INFO INIT: starting to scrape')
    if light_scrape:
        print('INFO INIT: light scraping mode selected')
        islamicbook_scrape.scrape_all(1)
        # news_scrape.scrape_all(1)
        chi3r_scrape.scrape_all(1)
    else:
        print('INFO INIT: heavy scrape mode selected')
        print('INFO INIT: islamicbook scrapping started')
        islamicbook_scrape.scrape_all()
        print('INFO INIT: islamicbook scrapping finished')
        print('INFO INIT: news scrapping started')
        news_scrape.scrape_all()
        print('INFO INIT: news scrapping finished')
        print('INFO INIT: chi3r scrapping started')
        chi3r_scrape.scrape_all()
        print('INFO INIT: chi3r scrapping finished')
        print('INFO INIT: shamela scrapping started')
        shamela_scrape.scrape_all()
        print('INFO INIT: shamela scrapping finished')

    print('INFO INIT: scrapping finished')

    print('INFO INIT: cleaning started')
    # cleaning
    cleaner.clean()

    print('INFO INIT: cleaning finished')

    print('INFO INIT: converting to xml started')
    # convert to xml
    if not os.path.isdir(xmlDir):
        os.makedirs(xmlDir)  # line B
    cleaner.convertScrapedToXml(xmlDir)

    print('INFO INIT: converting to xml finished')

    print ('INFO INIT: initializer finished')
