#!/usr/bin/env python

import sys
import io

from os import path

from hoccorpus import load_hoccorpus

def main(argv):
    if len(argv) != 3:
        print >> sys.stderr, 'Usage: hoccorpus2ann INDIR OUTDIR'
        return 1
    indir, outdir = argv[1:]

    if not path.isdir(outdir):
        print >> sys.stderr, '%s is not a directory' % outdir
        return 1

    documents = load_hoccorpus(indir)
    
    for d in documents:
        txtout = path.join(outdir, d.id+'.txt')
        with io.open(txtout, 'wt', encoding='utf-8') as out:
            out.write(d.text)
        annout = path.join(outdir, d.id+'.ann')
        with io.open(annout, 'wt', encoding='utf-8') as out:
            out.write(u'\n'.join(d.to_standoff()))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
