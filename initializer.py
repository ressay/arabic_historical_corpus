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


def scrape(limit_shamela=-1, limit_chi3r=-1, limit_news=-1, limit_islamic=-1):
    print('INFO INTI: quran is already scrapped, just creating xml')
    id_start = quran_corpus_builder.build(1, xmlDir)

    #Islamic
    print('INFO INIT: islamicbook scrapping started')
    if not limit_islamic:
        created_islamic, existed_islamic, errors_islamic = (0,0,0)
    else:
        created_islamic, existed_islamic, errors_islamic = islamicbook_scrape.scrape_all(limit_islamic)
    print('INFO INIT: created islamic', created_islamic)
    print('INFO INIT: existed islamic', existed_islamic)
    print('INFO INIT: errors islamic', errors_islamic)
    print('INFO INIT: islamicbook scrapping finished')

    # print('INFO INIT: cleaning islamic started')
    # cleaner.clean()
    # print('INFO INIT: cleaning islamic finished')
    #
    # print('INFO INIT: converting islamic to xml started')
    # id_start = cleaner.convertScrapedToXml(xmlDir, id_start + 1)
    # print('INFO INIT: converting islamic to xml finished')

    #News
    print('INFO INIT: news scrapping started')
    if not limit_news:
        created_news, existed_news, errors_news = (0,0,0)
    else:
        created_news, existed_news, errors_news = news_scrape.scrape_all(limit_news)
    print('INFO INIT: created news', created_news)
    print('INFO INIT: existed news', existed_news)
    print('INFO INIT: errors news', errors_news)
    print('INFO INIT: news scrapping finished')

    # print('INFO INIT: cleaning news started')
    # cleaner.clean()
    # print('INFO INIT: cleaning news finished')
    #
    # print('INFO INIT: converting news to xml started')
    # id_start = cleaner.convertScrapedToXml(xmlDir, id_start + 1)
    # print('INFO INIT: converting news to xml finished')

    #Chi3r
    print('INFO INIT: chi3r scrapping started')
    if not limit_chi3r:
        created_chi3r, existed_chi3r, errors_chi3r = (0,0,0)
    else:
        created_chi3r, existed_chi3r, errors_chi3r = chi3r_scrape.scrape_all(limit_chi3r)
    print('INFO INIT: created chi3r', created_chi3r)
    print('INFO INIT: existed chi3r', existed_chi3r)
    print('INFO INIT: errors chi3r', errors_chi3r)
    print('INFO INIT: chi3r scrapping finished')

    # print('INFO INIT: cleaning chi3r started')
    # cleaner.clean()
    # print('INFO INIT: cleaning chi3r finished')
    #
    # print('INFO INIT: converting chi3r to xml started')
    # cleaner.convertScrapedToXml(xmlDir, id_start + 1)
    # print('INFO INIT: converting chi3r to xml finished')

    # Shamela
    print('INFO INIT: shamela scrapping started')
    if not limit_shamela:
        created_shamela, existed_shamela, errors_shamela = (0,0,0)
    else:
        created_shamela, existed_shamela, errors_shamela = shamela_scrape.scrape_all()
    print('INFO INIT: created shamela', created_shamela)
    print('INFO INIT: existed shamela', existed_shamela)
    print('INFO INIT: errors shamela', errors_shamela)
    print('INFO INIT: shamela scrapping finished')

    print('INFO INIT: cleaning shamela started')
    cleaner.clean()
    print('INFO INIT: cleaning shamela finished')

    print('INFO INIT: converting shamela to xml started')
    id_start = cleaner.convertScrapedToXml(xmlDir, id_start + 1)
    print('INFO INIT: converting shamela to xml finished')

    created = created_chi3r + created_islamic + created_news #+ created_shamela
    existed = existed_chi3r + existed_islamic + existed_news #+ existed_shamela
    errors = errors_chi3r + errors_islamic + errors_news #+ errors_shamela

    return created, existed, errors

def convert():
    # convert to xml
    if not os.path.isdir(xmlDir):
        os.makedirs(xmlDir)  # line B

if __name__ == "__main__":
    import islamicbook_scrape
    import news_scrape
    import chi3r_scrape
    import shamela_scrape
    import cleaner
    import quran_corpus_builder
    import os

    cpt = quran_corpus_builder.build(1,xmlDir)
    # cleaner.convertScrapedToXml(xmlDir,cpt)
    # exit(0)
    print ('INFO INIT: initializer started')

    createDirectories()
    light_scrape = False

    options, remainder = getopt.getopt(sys.argv[1:], 'l:x:r',[])
    for opt,arg in options:
        if opt == '-l':
            light_scrape = True
        if opt == '-x':
            if not os.path.isdir(arg):
                print('ERROR: PATH ', arg, ' DOES NOT EXIST')
                exit(1)
            xmlDir = arg + '/xmlCorpus'  # where to put xml files
        if opt == '-r':
            if not os.path.isdir(arg):
                print('ERROR: PATH ', arg, ' DOES NOT EXIST')
                exit(1)
            path = arg + "/rawData"  # where to put scraped files


    print('INFO INIT: starting to scrape')
    if light_scrape:
        print('INFO INIT: light scraping mode selected')
        created, existed, errors = scrape(limit_shamela=0, limit_chi3r=10,
                                          limit_islamic=2, limit_news=0)
    else:
        print('INFO INIT: heavy scrape mode selected')
        created, existed, errors = scrape()


    print('INFO INIT: scrapping finished')
    print('INFO INIT: created', created)
    print('INFO INIT: existed', existed)
    print('INFO INIT: errors', errors)

    print ('INFO INIT: initializer finished')
