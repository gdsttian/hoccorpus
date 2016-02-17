#!/usr/bin/env python

# Split HoCCorpus documents into positive and negative sentences
# for a given label.

import sys
import io

from os import path

from hoccorpus import load_hoccorpus

def main(argv):
    if len(argv) != 4:
        print >> sys.stderr, 'Usage: hoccorpus2posneg INDIR LABEL OUTFN'
        return 1
    indir, label, outfn = argv[1:]

    documents = load_hoccorpus(indir)

    posfn, negfn = outfn + '.pos', outfn + '.neg'
    with io.open(posfn, 'wt', encoding='utf-8') as posout:
        with io.open(negfn, 'wt', encoding='utf-8') as negout:
            for d in documents:
                for s in d.sentences:
                    out = posout if label in s.labels else negout
                    print type(s.text)
                    out.write(s.text + u'\n')

if __name__ == '__main__':
    sys.exit(main(sys.argv))
