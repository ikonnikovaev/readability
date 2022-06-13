import re

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

text = input()
if is_hard(text):
    print('HARD')
else:
    print('EASY')
