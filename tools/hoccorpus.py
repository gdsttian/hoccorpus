import io
import re

from os import path
from glob import glob

class FormatError(Exception):
    pass

class Document(object):
    def __init__(self, id_, sentences):
        self.id = id_
        self.sentences = sentences

    @property
    def text(self):
        return ' '.join(s.text for s in self.sentences)

    def to_standoff(self):
        """Return list of annotation strings in the .ann standoff format."""
        offset, anns = 0, []
        for idx, s in enumerate(self.sentences, start=1):
            anns.extend(s.to_standoff(offset, idx))
            offset += len(s.text) + 1
        return anns

class Sentence(object):
    def __init__(self, text, labels):
        self.text = text
        self.labels = labels

    def to_standoff(self, offset, idx):
        """Return list of annotation strings in the .ann standoff format."""
        anns = []
        anns.append(u'T%d\tSentence %d %d\t%s' %
                    (idx, offset, offset+len(self.text), self.text))
        if self.labels:
            anns.append(u'A%d\tLabels T%d %s' %
                        (idx, idx, labels_to_string(self.labels)))
        return anns

def parse_labels(labelstr):
    labels = labelstr.strip('[]').split(', ')
    return [l.strip("'") for l in labels if l]

def labels_to_string(labels):
    return '--'.join(l.replace(' ', '-') for l in sorted(labels))

def read_document(flo, docid):
    """Read HoC corpus data from file-like-object, return Document.

    Each line in the HoC corpus consists of two TAB-separated fields,
    TEXT and LABELS, where TEXT is the text of a sentence and LABELS
    has the format

        ['LABEL1', 'LABEL2', ...]

    """
    sentences = []
    for ln, line in enumerate(flo, start=1):
        line = line.rstrip()
        fields = line.split('\t')
        if len(fields) != 2:
            raise FormatError('expected 2 fields, got %d: %s' %
                              (len(fields), line))
        text, labels = fields
        labels = parse_labels(labels)
        sentences.append(Sentence(text, labels))
    return Document(docid, sentences)
        
def load_document(fn):
    with io.open(fn, encoding='utf-8') as f:
        docid = path.splitext(path.basename(fn))[0]
        return read_document(f, docid)

def load_hoccorpus(directory):
    documents = []
    for fn in glob(path.join(directory, '*.txt')):
        documents.append(load_document(fn))
    return documents

if __name__ == '__main__':
    import sys
    documents = load_hoccorpus(sys.argv[1])
    for d in documents:
        print '\n'.join(d.to_standoff())
