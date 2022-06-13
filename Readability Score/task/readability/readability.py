# write your code here
def is_simple(text):
    if len(text) > 100:
        return False
    return True

text = input()
if is_simple(text):
    print('EASY')
else:
    print('HARD')
