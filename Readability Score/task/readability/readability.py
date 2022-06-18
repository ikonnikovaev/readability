import re
import math
import argparse

def avg(a):
    return sum(a) / len(a)


def sentence_len(sentence):
    words = [w for w in re.split(r'\s', sentence) if w]
    return len(words)

def is_hard(text):
    threshold = 10
    punct = r'[.?!]'
    sentences = [s for s in re.split(punct, text) if s]
    # print(sentences)
    avg_sentence_len = avg([sentence_len(s) for s in sentences])
    # print(avg_sentence_len)
    if avg_sentence_len > threshold:
        return True
    else:
        return False

def age_by_ari(ari):
    dict = {1: '5-6', 2: '6-7', 3: '7-9', 4: '9-10', 5: '10-11',
            6: '11-12', 7: '12-13', 8: '13-14', 9: '14-15', 10: '15-16',
            11: '16-17', 12: '17-18', 13: '18-24', 14: '24+'}
    return dict[math.ceil(ari)]

def calc_ari(text):
    spaces = r'[ \n\t]'
    punct = r'[.?!]'
    n_chars = 0
    for ch in text:
        if re.match(spaces, ch):
            pass
        else:
            n_chars += 1

    sentences = [s for s in re.split(punct, text) if s]
    n_sentences = len(sentences)
    n_words = sum([sentence_len(s) for s in sentences])

    print(f'Words: {n_words}')
    print(f'Sentences: {n_sentences}')
    print(f'Characters: {n_chars}')

    score = 4.71 * n_chars / n_words + 0.5 * n_words / n_sentences - 21.43
    print(f'The score is: {round(score, 2)}')
    print(f'This text should be understood by {age_by_ari(score)} year olds.')



parser = argparse.ArgumentParser()
parser.add_argument('--infile')
args = parser.parse_args()
infile = open(args.infile)
text = infile.read()
calc_ari(text)
infile.close()
