import sys
import os
import re
try:
    import json
except ImportError:
    import simplejson as json


#from BeautifulSoup import BeautifulSoup as Soup

class MDTagger(object):
    ''' '''
    def __init__(self, lexfile, itemref=True):
        self.itemref = itemref
        self.lexfile = lexfile
        self.lexicon = None
        self.markup = None
        self.load_lexicon(lexfile)
        self.itemrefs = []

    def load_lexicon(self, lexfile):
        try:
            self.lexicon = json.load(open(lexfile))
        except JSONDecodeError:
            sys.exit('Input lexicon was not valid JSON... exiting.')
        
    def tag_markup(self, markup):
        self.markup = markup
        for semtype in self.lexicon:
            for s in self.lexicon[semtype]:
                pattern = self.make_pattern(s)
                self.apply_pattern(pattern)
        
    def apply_pattern(self, p):
        pattern = re.compile(p, re.I|re.M|re.S)
        matches = re.findall(pattern, self.markup)
        print 'Num matches:', len(matches)
        for match in matches:
            self.handle_match(match)

    def make_pattern(self, s):
        ws = r'[ \t\r\n]'
        tag = r'<[^>]*>'
        junk = r'(%s|%s)*' % (ws, tag)
        pattern = junk + junk.join(['('+name+')' for name in s.split()]) + junk  
        print 'Pattern:', pattern
        return pattern

    def handle_match(self, match):
        print 'Match:', match
        if self.itemref:
            self.make_itemref_item(match)
        else:
            self.make_item(match)

if __name__ == '__main__':
    tagger = MDTagger('sample-lexicon.json')
    markup = open('sample-markup.html').read()
    tagger.tag_markup(markup)
