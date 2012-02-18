import sys
import os
import re
try:
    import json
except ImportError:
    import simplejson as json

class MicrodataTagger(object):
    ''' '''
    def __init__(self, lexfile, opt_textmode=True, opt_nameparts=False):
        self.lexfile = lexfile
        self.opt_textmode = opt_textmode
        self.opt_nameparts = opt_nameparts
        self.lexicon = None
        self.old_markup = None
        self.load_lexicon(lexfile)

    def load_lexicon(self, lexfile):
        try:
            self.lexicon = json.load(open(lexfile))
        except Exception:
            sys.exit('Input lexicon was not valid JSON... exiting.')
        
    def tag_markup(self, markup):
        self.old_markup = markup
        self.new_markup = re.sub(r'<[^>]*>', '', markup)
        for semtype in self.lexicon:
            for lexentry in self.lexicon[semtype]:
                pattern = self.make_pattern(lexentry)
                self.apply_pattern(pattern, semtype)
        if self.opt_textmode:
            return tagger.new_markup
        else:
            return self.merge_markups()

    def apply_pattern(self, pattern, semtype):
        def sub_callback(match):
            groups = match.groups()
            beg_tag = '<span itemscope itemtype="%s" itemprop="name">' % semtype
            end_tag = '</span>'
            return beg_tag + ''.join(groups) + end_tag
        pattern = re.compile(pattern, re.I|re.M|re.S)
        self.new_markup = re.sub(pattern, sub_callback, self.new_markup)

    def make_pattern(self, s):
        # Treat regex entry as regex literal
        if s.startswith('r:'):
            lex_regex_literal = s[2:]
            # Capture the entry if capture parens aren't present
            if not (lex_regex_literal.startswith('(') and lex_regex_literal.endswith('(')):
                pattern = '('+s[2:]+')'
        else:
            re_name_parts = []
            name_parts = s.split()
            for np_i in range(len(name_parts)):
                key = 'name_' + str(np_i)
                re_part = '(?P<%s>%s)' % (key, name_parts[np_i])
                re_name_parts.append(re_part)
            if self.opt_textmode:
                re_junk = r'([ \t\r\n]*)'
                pattern = re_junk.join(re_name_parts)
            else:
                re_junk = r'(<[^>]*>*|[ \t\r\n]*)'
                pattern = re_junk + re_junk.join(re_name_parts) + re_junk
        return pattern

if __name__ == '__main__':
    tagger = MicrodataTagger('sample-lexicon.json')
    tagger.nameparts = True
    markup = open('sample-text.txt').read()
    tagger.tag_markup(markup)
    print tagger.new_markup
