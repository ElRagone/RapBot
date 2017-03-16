#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import spacy
from spacy.symbols import ORTH, LEMMA, POS
from spacy.symbols import nsubj, VERB, dobj

nlp = spacy.load('en')

""" Added some common cases to the nlp instance that were not recognized """
nlp.tokenizer.add_special_case(u'gimme',
    [
        {
            ORTH: u'gim',
            LEMMA: u'give',
            POS: u'VERB'},
        {
            ORTH: u'me'}])

nlp.tokenizer.add_special_case(u'wanna',
    [
        {
            ORTH: u'wan',
            LEMMA: u'want',
            POS: u'VERB'},
        {
            ORTH: u'na'}])
    
nlp.tokenizer.add_special_case(u'niggas',
    [
        {
            ORTH: u'niggas',
            LEMMA: u'nigga',
            POS: u'NOUN'}])

nlp.tokenizer.add_special_case(u'Niggas',
    [
        {
            ORTH: u'niggas',
            LEMMA: u'nigga',
            POS: u'NOUN'}])

nlp.tokenizer.add_special_case(u'Nigga',
    [
        {
            ORTH: u'nigga',
            LEMMA: u'nigga',
            POS: u'NOUN'}])

""" Different semantic representations of a document.
    In the end, I did not use any of these representations, since there were
    little lines in which the POS was accurate enough and the features did not 
    add much more to the result than the average vector (while adding a lot of 
    computation time)"""    
def _average_vector(word_set):
    vectors = np.array([word.vector for word in word_set])
    return np.nanmean(vectors, axis=0)

def _subjects_vector(doc):
    subjects = set([token for token in doc if token.dep == nsubj])    
    return _average_vector(subjects)
            
def _objects_vector(doc):
    objects = set([token for token in doc if token.dep == dobj])                     
    return _average_vector(objects)

def _verbs_vector(doc):
    verbs = set([token for token in doc if token.pos == VERB])
    return _average_vector(verbs)

""" Wrapper for the cosine similarity function that handles cases where no
    vector existed. This function was mainly important for the subjects-, 
    objects- and verbs-vectors, due to the low occurrence of these POS'es """
def _compute_similarity(input_vector, ref_vector):
    if not type(input_vector) is np.ndarray and not type(ref_vector) is np.ndarray:
        return 1
    elif not type(input_vector) is np.ndarray or not type(ref_vector) is np.ndarray:
        return 0
    else:
        return cosine_similarity(input_vector.reshape(1, -1), ref_vector.reshape(1, -1))[0][0]

""" Jaccard similarity as a semantic BOW feature """
def _compute_jaccard(input_doc, doc):
    input_lemmas = {word.lemma_ for word in input_doc}
    ref_lemmas = {word.lemma_ for word in doc}
    
    intersect = len(input_lemmas.intersection(ref_lemmas))
    union = len(input_lemmas.union(ref_lemmas))
    
    return intersect / union

""" Computes the cosine similarity of the average GloVe vectors of the
    input line (the user's line) and the line from the data set, and computes
    the Jaccard similarity of the two lines """
def get_semantic_features(input_line, line):
    input_doc = nlp(str(input_line))
    doc = nlp(str(line))
    
    input_total = input_doc.vector
    total = doc.vector
    tot_cos = _compute_similarity(input_total, total)
    
    jaccard = _compute_jaccard(input_doc, doc)
    
    return jaccard, tot_cos