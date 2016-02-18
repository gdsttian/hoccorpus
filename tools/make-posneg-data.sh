#!/bin/bash

# Use hoccorpus2posneg.py to split HoC corpus data into files of
# positive and negative sentences with respect to each of the hallmarks.

set -e
set -u

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

indir=$1
outdir=$2

# check that train/devel/test split is found
for s in train devel test; do
    if [ ! -d "$indir/$s" ]; then
	echo "No $indir/$s directory"
	exit 1
    fi
done

for h in "activating invasion and metastasis" \
	     "avoiding immune destruction" \
	     "cellular energetics" \
	     "enabling replicative immortality" \
	     "evading growth suppressors" \
	     "genomic instability and mutation" \
	     "inducing angiogenesis" \
	     "resisting cell death" \
	     "sustaining proliferative signaling" \
	     "tumor promoting inflammation"; do
    o="$outdir/hoc-"${h// /-}
    mkdir $o
    for s in train devel test; do
	python $SCRIPTDIR/hoccorpus2posneg.py "$indir/$s" "$h" "$o/$s"
    done
done
