import re
import math
import argparse

def avg(a):
    return sum(a) / len(a)

def text_to_sentences(text):
    punct = r'[.?!]'
    sentences = [s for s in re.split(punct, text) if s]
    return sentences

def sentences_in_text(text):
    sentences = text_to_sentences(text)
    return len(sentences)

def chars_in_text(text):
    spaces = r'[ \n\t]'
    n_chars = 0
    for ch in text:
        if re.match(spaces, ch):
            pass
        else:
            n_chars += 1
    return n_chars

def sentence_to_words(sentence):
    words = [w for w in re.split(r'\s', sentence) if w]
    return words

def words_in_sentence(sentence):
    words = sentence_to_words(sentence)
    return len(words)

def words_in_text(text):
    sentences = text_to_sentences(text)
    n_words = sum([words_in_sentence(s) for s in sentences])
    return n_words

def syllables_in_word(word):
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

def syllables_in_text(text):
    n_syllables = 0
    sentences = text_to_sentences(text)
    for s in sentences:
        words = sentence_to_words(s)
        for w in words:
            n_syllables += syllables_in_word(w)
    return n_syllables

def polysyllables_in_text(text):
    n_polysyllables = 0
    sentences = text_to_sentences(text)
    for s in sentences:
        words = sentence_to_words(s)
        for w in words:
            k = syllables_in_word(w)
            if k > 2:
                n_polysyllables += 1
    return n_polysyllables

def is_hard(text):
    threshold = 10
    punct = r'[.?!]'
    sentences = [s for s in re.split(punct, text) if s]
    # print(sentences)
    avg_sentence_len = avg([words_in_sentence(s) for s in sentences])
    # print(avg_sentence_len)
    if avg_sentence_len > threshold:
        return True
    else:
        return False

def age_by_score(score):
    # dict = {1: '5-6', 2: '6-7', 3: '7-9', 4: '9-10', 5: '10-11',
            #6: '11-12', 7: '12-13', 8: '13-14', 9: '14-15', 10: '15-16',
            #11: '16-17', 12: '17-18', 13: '18-24', 14: '24+'}
    if score < 3:
        return score + 5
    elif score < 13:
        return score + 6
    elif score == 13:
        return 24
    return 25



def calc_ari(n_chars, n_words, n_sentences):
    score = 4.71 * n_chars / n_words + 0.5 * n_words / n_sentences - 21.43
    return math.ceil(score)

def calc_fk(n_syllables, n_words, n_sentences):
    score = 0.39 * n_words/ n_sentences + 11.8 * n_syllables / n_words - 15.59
    return math.ceil(score)

def calc_cl(n_chars, n_words, n_sentences):
    l = 100 * n_chars / n_words
    s = 100 * n_sentences / n_words
    score = 0.0588 * l - 0.296 * s - 15.8
    return math.ceil(score)



parser = argparse.ArgumentParser()
parser.add_argument('--infile')
args = parser.parse_args()
infile = open(args.infile)
text = infile.read()
infile.close()


n_chars = chars_in_text(text)
n_sentences = sentences_in_text(text)
n_words = words_in_text(text)
n_syllables = syllables_in_text(text)
n_polysyllables = polysyllables_in_text(text)
print(f'Words: {n_words}')
print(f'Sentences: {n_sentences}')
print(f'Characters: {n_chars}')
print(f'Syllables: {n_syllables}')
print(f'Polysyllables: {n_polysyllables}')

print('Enter the score you want to calculate (ARI, FK, CL, all):')
indices = input().split()
if 'all' in indices:
    indices = ['ARI', 'FK', 'CL']
ages = []
for ind in indices:
    if ind == 'ARI':
        ari = calc_ari(n_chars, n_words, n_sentences)
        age = age_by_score(ari)
        ages.append(age)
        print(f'Automated Readability Index: {ari} (about {age} year olds).')
    elif ind == 'FK':
        fk = calc_fk(n_syllables, n_words, n_sentences)
        age = age_by_score(fk)
        ages.append(age)
        print(f'Flesch–Kincaid readability tests: {fk} (about {age} year olds).')
    elif ind == 'CL':
        cl = calc_cl(n_chars, n_words, n_sentences)
        age = age_by_score(cl)
        ages.append(age)
        print(f'Coleman–Liau index: {cl} (about {age} year olds).')
avg_age = avg(ages)
print(f'This text should be understood in average by {round(avg_age, 0)} year olds.')

