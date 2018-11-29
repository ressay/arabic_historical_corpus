from nltk.corpus import XMLCorpusReader
import nltk

class HistoricalCorpus(XMLCorpusReader):


    def sents(self):
        sents = self.words()
        return sents