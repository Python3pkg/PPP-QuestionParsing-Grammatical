#!/usr/bin/env python3

import requests
import sys

from conceptnet5.nodes import normalized_concept_name, uri_to_lemmas
from conceptnet5.query import lookup
# https://github.com/commonsense/conceptnet5/blob/master/conceptnet5/nodes.py
# https://github.com/commonsense/conceptnet5/wiki/API

# How to test in a terminal : 
#   python3
#   from conceptnet2 import *
#   associatedWords('elected','/r/RelatedTo')
#   normalize('elected')

# Run `./conceptnet.py banana` to search words related to banana.

default_language = 'en'

def normalize(language,word):
    return normalized_concept_name(language, word)

def associatedWords(uri,relations):
    """
        Return words related to the given word by the given relations.
    """
    r = list(lookup(uri,limit=100))
    node = [w['start'] for w in r 
                       if w['end'] == uri
                          and w['rel'] in relations 
                          and w['start'].startswith('/c/'+default_language)]
    node = [' '.join(uri_to_lemmas(w)) for w in node if '_' not in w]
    return set(node)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Syntax: ./%s <word to search>" % sys.argv[0])
    word=normalize(default_language,sys.argv[1])
    uri = "/c/{0}/{1}".format(default_language,word)
    print(associatedWords(uri,{'/r/RelatedTo'}))
    #print(associatedWords(uri,{'/r/CapableOf'},{'/r/RelatedTo', '/r/Synonym', '/r/Causes', '/r/DerivedFrom'}))
