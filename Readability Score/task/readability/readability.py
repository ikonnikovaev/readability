import re
import math
import argparse

import argparse
import math
import re

class TextInfo:
    def __init__(self, text, simple_words):
        self.text = text
        self.sentences = self.to_sentences()
        self.words = self.to_words()
        self.n_sentences = len(self.sentences)
        self.n_words = len(self.words)
        self.n_chars = self.count_chars()
        self.n_syllables = self.count_syllables()
        self.n_polysyllables = self.count_polysyllables()
        self.n_difficult = self.count_difficult(simple_words)

    def count_chars(self):
        spaces = r'[ \n\t]'
        n_chars = 0
        for ch in self.text:
            if re.match(spaces, ch):
                pass
            else:
                n_chars += 1
        return n_chars

    def to_sentences(self):
        punct = r'[.?!]'
        sentences = [s for s in re.split(punct, text) if s]
        return sentences

    def to_words(self):
        words = []
        for sentence in self.sentences:
            words.extend([w for w in re.split(r'[.!?(),\s]+', sentence) if w])
        return words

    def count_syllables_in_word(self, word):
        vowels = 'aeiouy'
        n_syllables = 0
        for i in range(len(word)):
            if word[i] in vowels:
                if i > 0 and word[i - 1] in vowels:
                    pass
                elif i == len(word) - 1 and word[i] == 'e':
                    pass
                else:
                    n_syllables += 1
        return max(n_syllables, 1)

    def count_syllables(self):
        return sum([self.count_syllables_in_word(w) for w in self.words])

    def count_polysyllables(self):
        n_polysyllables = 0
        for w in self.words:
            k = self.count_syllables_in_word(w)
            if k > 2:
                n_polysyllables += 1
        return n_polysyllables

    def count_difficult(self, simple_words):
        n_difficult = 0
        for word in self.words:
            if not word.lower() in simple_words:
                n_difficult += 1
        return n_difficult

    def print_info(self):
        print(f'Words: {self.n_words}')
        print(f'Difficult words: {self.n_difficult}')
        print(f'Sentences: {self.n_sentences}')
        print(f'Characters: {self.n_chars}')
        print(f'Syllables: {self.n_syllables}')
        print(f'Polysyllables: {self.n_polysyllables}')


def avg(a):
    if not a:
        return 0
    return sum(a) / len(a)

class ReadabilityScorer:
    def __init__(self, text_info):
        self.text_info = text_info

    def calc_ari(self):
        score = 4.71 * self.text_info.n_chars / self.text_info.n_words
        score += 0.5 * self.text_info.n_words / self.text_info.n_sentences
        score -= 21.43
        return math.ceil(score)

    def calc_fk(self):
        score = 0.39 * self.text_info.n_words / self.text_info.n_sentences
        score += 11.8 * self.text_info.n_syllables / self.text_info.n_words
        score -= 15.59
        return math.ceil(score)

    def calc_smog(self):
        score = 1.043 * math.sqrt(self.text_info.n_polysyllables * 30 / self.text_info.n_sentences) + 3.1291
        return math.ceil(score)

    def calc_cl(self):
        l = 100 * self.text_info.n_chars / self.text_info.n_words
        s = 100 * self.text_info.n_sentences / self.text_info.n_words
        score = 0.0588 * l - 0.296 * s - 15.8
        return math.ceil(score)

    def calc_dc(self):
        p = self.text_info.n_difficult / self.text_info.n_words
        score = 0.1579 * p * 100 + 0.0496 * self.text_info.n_words / self.text_info.n_sentences
        if p < 0.05:
            pass
        else:
            score += 3.6365
        return round(score, 2)

    def score_to_age(self, score):
        if score < 3:
            return score + 5
        elif score < 13:
            return score + 6
        elif score == 13:
            return 24
        return 25

    def score_to_age_for_dc(self, score):
        if score < 5.0:
            return 10
        if score < 6.0:
            return 12
        if score < 7.0:
            return 14
        if score < 8.0:
            return 16
        if score < 9.0:
            return 18
        return 24



parser = argparse.ArgumentParser()
parser.add_argument('--infile')
parser.add_argument('--words')
args = parser.parse_args()

words_file = open(args.words)
simple_words = words_file.read().split()
words_file.close()

text_file = open(args.infile)
text = text_file.read()
text_file.close()

text_info = TextInfo(text, simple_words)
text_info.print_info()

scorer = ReadabilityScorer(text_info)

print('Enter the score you want to calculate (ARI, FK, SMOG, CL, DC, all):')
indices = input().split()
if 'all' in indices:
    indices = ['ARI', 'FK', 'SMOG', 'CL', 'DC']
ages = []
for ind in indices:
    ind = ind.upper()
    if ind == 'ARI':
        ari = scorer.calc_ari()
        age = scorer.score_to_age(ari)
        ages.append(age)
        print(f'Automated Readability Index: {ari} (about {age} year olds).')
    elif ind == 'SMOG':
        smog = scorer.calc_smog()
        age = scorer.score_to_age(smog)
        ages.append(age)
        print(f'Simple Measure of Gobbledygook: {smog} (about {age} year olds).')
    elif ind == 'FK':
        fk = scorer.calc_fk()
        age = scorer.score_to_age(fk)
        ages.append(age)
        print(f'Flesch–Kincaid readability tests: {fk} (about {age} year olds).')
    elif ind == 'CL':
        cl = scorer.calc_cl()
        age = scorer.score_to_age(cl)
        ages.append(age)
        print(f'Coleman–Liau index: {cl} (about {age} year olds).')
    elif ind == 'DC':
        dc = scorer.calc_dc()
        age = scorer.score_to_age_for_dc(dc)
        ages.append(age)
        print(f'Dale-Chall score: {dc} (about {age} year olds).')

avg_age = avg(ages)
print(f'This text should be understood in average by {round(avg_age, 0)} year olds.')

