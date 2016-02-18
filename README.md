# HoCCorpus

Hallmarks of Cancer corpus data and tools.

## Data

- `original-data/`: HoCCorpus data downloaded from
  <http://www.cl.cam.ac.uk/~sb895/HoC.html>.

- `fixenc-data/`: HoCCorpus data with encoding issues fixed using

        for f in original-data/*; do
            python tools/fixhocencoding.py $f > fixenc-data/`basename $f`;
        done

- `pubmed-data/`: PubMed XML source for HoCCorpus articles.

- `pubmed-tiabs/`: Titles and abstracts of HoCCorpus articles, derived from
  `pubmed-data/` source using `extractTIABs.py -nc` with script from
  <https://github.com/spyysalo/pubmed>.

- `split/`: 50/17/33% train/devel/test split of documents (ID lists).

- `split-data/`: Corpus data split per `split/{train,devel,test}.txt`

## Tools

- `tools/fixhocencoding.py`: Fix doubly-encoded UTF-8 and XML escapes
  in text.

- `tools/hoccorpus2ann.py`: Convert source data to .ann standoff
  format.

- `tools/hoccorpus2posneg.py`: Convert source data to text files containing
  positive and negative sentences for a given label (hallmark).
