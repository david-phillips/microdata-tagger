import sys
import os
import re
try:
    import json
except ImportError:
    import simplejson as json

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
                self.apply_pattern(pattern, semtype)
        
    def apply_pattern(self, p, semtype):
        pattern = re.compile(p, re.I|re.M|re.S)
        for match in re.finditer(pattern, self.markup):
            self.handle_match(match, semtype)

    def make_pattern(self, s):
        re_junk = r'(<[^>]*>*|[ \t\r\n]*)'
        re_name_parts = []
        name_parts = s.split()
        for np_i in range(len(name_parts)):
            key = 'name_' + str(np_i)
            re_part = '(?P<%s>%s)' % (key, name_parts[np_i])
            re_name_parts.append(re_part)
        pattern = re_junk + re_junk.join(re_name_parts) + re_junk
        return pattern

    def handle_match(self, match, semtype):
        groups = match.groups()
        pre_junk = groups[0]
        post_junk = groups[len(groups)-1]
        if len(groups) < 3:
            return
        # We've processed this already
        if 'itemscope' in pre_junk:
            return
        beg_tag_pos = match.start() + len(pre_junk)
        end_tag_pos = match.end() - len(post_junk)
        beg_tag = '<span itemscope itemtype="%s" itemprop="name">' % semtype
        end_tag = '</span>'
        self.markup = self.markup[:beg_tag_pos] + beg_tag +\
                      self.markup[beg_tag_pos:end_tag_pos] + end_tag +\
                      self.markup[end_tag_pos:]
        
        
        

if __name__ == '__main__':
    tagger = MDTagger('sample-lexicon.json')
    markup = open('sample-markup.html').read()
    tagger.tag_markup(markup)
