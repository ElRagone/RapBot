#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE

import re

""" All vowel symbols of the International Phonetic Alphabet """
VOWELS = r'i|ɪ|e|ɛ|æ|a|ə|ɑ|ɒ|ɔ|ʌ|o|ʊ|u|y|ʏ|ø|œ|ɐ|ɜ|ɞ|ɘ|ɵ|ʉ|ɨ|ɤ|ɯ'

""" Calculate IPA phonetic strings of a line. Phon_words returns the phonetic
    vowel symbols per word and phon_concat returns all phonetic vowels of the
    line joined and reversed order. The phonetic strings are determined using
    the espeak application """
def get_phonemes(line):
    line = re.sub(r'"', '', line)
    
    command = 'espeak --ipa -q "{}"'.format(line)
    process = Popen(command, shell=True, stdout=PIPE)
    
    output, _ = process.communicate()
    output = str(output, encoding='utf-8')
    
    phon_words = [re.sub('[^{}]'.format(VOWELS), '', word) for word in output.split()]
    phon_concat = ''.join(re.findall(VOWELS, output))[::-1]
    
    return phon_words, phon_concat

""" Calculate the rhyme features of the user defined input line and a line
    from the data set. End_rhyme is the length of common vowel symbols at the
    end of both lines. Total rhyme averages the max common vowel substring for
    each word in the user defined input line """
def get_rhyme_features(input_line, line):
    phon_words, phon_concat = get_phonemes(line)
    input_phon_words, input_phon_concat = get_phonemes(input_line)
    
    end_rhyme = len(os.path.commonprefix([input_phon_concat, phon_concat]))
       
    total_rhyme = 0
    for input_word in input_phon_words:
        max_len = 0
        for word in phon_words:
            current_len = len(os.path.commonprefix([input_word, word]))
            if current_len > max_len:
                max_len = current_len
        total_rhyme += max_len
    total_rhyme /= len(input_phon_words)
    
    return end_rhyme, total_rhyme