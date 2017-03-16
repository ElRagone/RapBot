# Rap Bot

## Description

Rap Bot is a Python bot that generates rap lines that best fit a sentence given by the user. The approach of the bot is based on the DopeLearning paper of Malmi, Takali, Toivonen, Raiko and Gionis (2016) - <https://arxiv.org/pdf/1505.04771.pdf>.

## Data

The data set consists of around 500,000 lines from rap lyrics of over  100 rappers. The lyrics were crawled from Genius.com using the *Crawler* notebook I created.

## Features

The bot uses five features to rank the lines:

#### Semantic Features
- **Jaccard Similarity** of the user's line and the suggested line.
- The **cosine similarity** of the average **GloVe vectors** of the user's line and the suggested line.

#### Phonetic Features
- The number of phonetic vowel symbols the suffix of the user's line and suggested line have in common, which is an approximation of their **End Rhyme**.
- The length of the longest substring of phonetic vowel symbols found in the user's line averaged over each word in the suggested line. This captures **other** forms of **rhymes**.

#### Other Features
- The inverse normalized difference in the **character lenght** of the user's line and the suggested line.

## Ranking
First the bot selects a subset of candidate lines from the data set. This can be done randomly or by selecting the subset which rhymes the best with user's line (based on end rhyme). This subset is then ranked using a linear RankSVM classifier. RankSVM was trained using pairwise transforms, where the next line of a lyric was considered the ground truth which should be ranked above a random other line.

## Dependencies
- The phonetic features are extracted using the *eSpeak* command line application (<http://espeak.sourceforge.net/>).
- Natural language processing was done using the *Spacy* Python library (<https://spacy.io/>).

## Files
- Crawler.ipynb - Notebook used to crawl the lyrics.
- Extract Phonemes.ipynb - Notebook used to expand the lyrics data set with phonetic features.
- Feature Training.ipynb - Notebook used to train the RankSVM classifier (Because training/testing took a long time, I was only able to train the classifier on a small subset of the data and was not able to get recall values at different intervals for the test set).
- lyrics_sorted.csv - Lyrics dataset, which is sorted on the reverse of the concatenated string of phonetic vowel symbols.
- RapBot.py, LineRanking.py, PhoneticFeatures.py and SemanticFeatures.py - Source files of the bot

## Example Lines
![Examples](http://i.imgur.com/D6SMyIc.png)
