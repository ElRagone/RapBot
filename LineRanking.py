#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import os
import string

from PhoneticFeatures import get_rhyme_features, get_phonemes
from SemanticFeatures import get_semantic_features

""" Load the lyrics data set. The data set is sorted on the phonetic vowel
    symbols of each line """
lyrics = pd.read_csv('lyrics_sorted.csv')

""" Gets a slice of the data set containing the closest neighbours for a 
    given index """
def _get_slice(index, lyrics, k):
    lower = index - k / 2
    upper = index + k / 2 - 1
    
    if lower < 0:
        upper += -1 * lower
        lower = 0
    elif upper > lyrics.shape[0] - 1:
        lower -= upper - lyrics.shape[0] - 1
        upper = lyrics.shape[0] - 1
          
    return lyrics.loc[lower:upper]

""" Selects candidates based on the end rhyme of the lines """
def _select_candidates(input_phon, lyrics, k):
    max_prefix = (0, 0)
    
    for i, phon in enumerate(lyrics.Vowels):
        prefix_len = len(os.path.commonprefix([input_phon, phon]))
        if prefix_len > max_prefix[1]:
            max_prefix = (i, prefix_len)
    
    return _get_slice(max_prefix[0], lyrics, k)

""" Calculate the feature values for a line from the data set """
def _calculate_features(input_line, line, semantic=True, rhyme=True, length=True):
    print('Calculating Features...')
    translator = str.maketrans('', '', string.punctuation)

    line = line.translate(translator)
    input_line = input_line.translate(translator)
    
    # Semantic features
    jaccard, total = get_semantic_features(input_line, line)
    
    # Rhyming features
    end_rhyme, total_rhyme = get_rhyme_features(input_line, line)
    
    # Other features
    length = 1 - abs(len(input_line) - len(line)) / max(len(input_line), len(line))
    
    #return np.array([subjects, objects, verbs, total, end_rhyme, total_rhyme, length])
    return np.array([jaccard, total, end_rhyme, total_rhyme, length])

""" Get the candidate line withh the highest score. The default coefficients
    are based on RankSVM """
def get_best_line(input_line, coef=[0.68, 0.12, -0.67, 0.08, 0.18], k=100, random_candidates=False):
    # Mean and standard deviation of the the trianing data
    mean = [0.05618665, 0.72029447, 1.11975, 0.71374178, 0.7401983]
    std = [0.10824952, 0.15384646, 1.13375921, 0.27429371, 0.1920263]
    
    _, input_phonemes = get_phonemes(input_line)
    
    if not random_candidates:
        candidates = _select_candidates(input_phonemes, lyrics, k)
    else:
        candidates = lyrics.sample(n=k)
        
    semantic = coef[0] != 0 or coef[1] != 0
    rhyme = coef[2] != 0 or coef[3] != 0
    length = coef[4] != 0
    
    best = (0, '')
    for _, candidate in candidates.iterrows():
        features = _calculate_features(input_line, candidate.Line,
                                       semantic=semantic, rhyme=rhyme, lenght=length)
        features = (features - mean) / std
        score = np.dot(coef, features)
        if score > best[0] and candidate.Line != input_line:
            best = (score, candidate.Line)
    
    return best[1]