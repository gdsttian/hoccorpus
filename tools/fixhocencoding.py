#!/usr/bin/env python

# Fix encoding issues in HoCCorpus source data.

# Specifically, unescape XML escapes and decode doubly-encoded UTF-8.

import sys
import re
import io

XML_UNESCAPES = {
    '&lt;' : '<',
    '&gt;' : '>',
    '&amp;' : '&',
    # The data contains also broken variants with an extra space
    '&lt ;' : '<',
    '&gt ;' : '>',
    '&amp ;' : '&',
}

def utf_decode(text, fn):
    # process split by space to minimize impact of decode errors
    tokens = text.split(' ')
    decoded = []
    for t in tokens:
        try:
            # http://stackoverflow.com/a/1177542
            t = t.encode('raw_unicode_escape').decode('utf-8')
        except UnicodeDecodeError, e:
            print >> sys.stderr, 'Decode error in %s: "%s"' % (fn, t)
            pass
        decoded.append(t)
    return ' '.join(decoded)

def xml_unescape(text, fn):
    for e, u in XML_UNESCAPES.items():
        text = text.replace(e, u)
    return text

def process(fn, out=None):
    if out is None:
        out = sys.stdout
    with io.open(fn, encoding='utf-8') as f:
        text = f.read()
    text = utf_decode(text, fn)
    text = xml_unescape(text, fn)
    out.write(text.encode('utf-8'))
    
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: fixhocencoding FILE [FILE ...]'
        return 1
    for fn in argv[1:]:
        process(fn)
    return 0
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
