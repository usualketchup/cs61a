""" Typing Test implementation """

from utils import *
from ucb import main

# BEGIN Q1-5
def lines_from_file(path):
    file = open(path, mode='r')
    readfile = readlines(file)
    readwords = [i.strip(' \n').strip(' \t ') for i in readfile]
    return readwords


def new_sample(path, i):
    return lines_from_file(path)[i]


def analyze(sample_paragraph, typed_string, start_time, end_time):
    split_text = split(sample_paragraph)
    split_user = split(typed_string)

    def words_per_minute(start_time, end_time, typed_string):
        time = end_time - start_time
        number = len(typed_string)/5
        wpm = number/time * 60
        return wpm

    def accuracy(split_text, split_user):
        total = min(len(split_user), len(split_text))

        def correct(split_text, split_user):
            if not split_text or not split_user:
                return 0
            elif split_text[0] == split_user[0]:
                return correct(split_text[1:], split_user[1:]) + 1
            else:
                return correct(split_text[1:], split_user[1:])
        right = correct(split_text, split_user)
        if total > 0:
            return right/total * 100
        else:
            return 0.0
    return [words_per_minute(start_time, end_time, typed_string), accuracy(split_text, split_user)]


def pig_latin(sample_paragraph):
    splited_paragraph = split(sample_paragraph)

    def pig_latin_vowel(x):
        return x + 'way'

    def pig_latin_consonant(x):
        cluster = ''
        conc_x = x
        for i in x:
            if i != 'a' and i != 'e' and i != 'i' and i != 'o' and i != 'u':
                cluster += i
                conc_x = conc_x[1:]
            else:
                break
        return conc_x+cluster+'ay'
    pl=''
    for x in splited_paragraph:
        if x[0] == 'a' or x[0] == 'e' or x[0] == 'i' or x[0] == 'o' or x[0] == 'u':
            pl += pig_latin_vowel(x)
        else:
            pl += pig_latin_consonant(x)
    return pl


def autocorrect(user_input, words_list, score_function):
    if user_input in words_list:
        return user_input
    else:
        min_value = min([score_function(user_input, word) for word in words_list])
        for word in words_list:
            if score_function(user_input, word) == min_value:
                return word


def swap_score(s1, s2):
    if not s1 or not s2:
        return 0
    elif s1[0] == s2[0]:
        return swap_score(s1[1:], s2[1:])
    else:
        return swap_score(s1[1:], s2[1:]) + 1


# END Q1-5

# Question 6

def score_function(word1, word2):
    """A score_function that computes the edit distance between word1 and word2."""
    if word1 == word2:  # Fill in the condition
        # BEGIN Q6
        return 0
        # END Q6
    elif not word2:
        return score_function(word1[1:], word2) + 1
    elif not word1:
        return score_function(word2[0], word2) + 1
    elif word1[0] == word2[0]:  # Feel free to remove or add additional cases
        return score_function(word1[1:], word2[1:])
    else:
        add_char = lambda: score_function(word2[0] + word1, word2) + 1 # Fill in these lines
        remove_char = lambda: score_function(word1[1:], word2) + 1
        substitute_char = lambda: score_function(word2[0] + word1[1:], word2) + 1
        if len(word1) < len(word2):
            if [c for c in range(len(word1)) if word1[c] == word2[c]]:
                return substitute_char()
            else:
                return add_char()
        elif len(word1) > len(word2) or len(word1) >= 2 and word1[1] == word2[0]:
            return remove_char()
        else:
            return substitute_char()
        # END Q6


KEY_DISTANCES = get_key_distances()
# BEGIN Q7-8


def score_function_accurate(word1, word2):
    if word1 == word2:
        return 0
    elif not word2:
        return score_function_accurate(word1[1:], word2) + 1
    elif not word1:
        return score_function_accurate(word2[0], word2) + 1
    elif word1[0] == word2[0]:
        return score_function_accurate(word1[1:], word2[1:])
    else:
        if len(word1) < len(word2):
            if [c for c in range(len(word1)) if word1[c] == word2[c]]:
                return score_function_accurate(word2[0] + word1[1:], word2) + 1
            else:
                return score_function_accurate(word2[0] + word1, word2) + 1
        elif len(word1) > len(word2) or len(word1) >= 2 and word1[1] == word2[0]:
            return score_function_accurate(word1[1:], word2) + 1
        else:
            substitute_char = KEY_DISTANCES[word1[0], word2[0]] + score_function_accurate(word1[1:], word2[1:])
            return substitute_char


def score_function_final(word1, word2):
    if word1 == word2:
        return 0
    elif not word2:
        return score_function_final(word1[1:], word2) + 1
    elif not word1:
        return score_function_final(word2[0], word2) + 1
    elif word1[0] == word2[0]:
        return score_function_final(word1[1:], word2[1:])
    else:
        if len(word1) < len(word2):
            if [c for c in range(len(word1)) if word1[c] == word2[c]]:
                return score_function_final(word2[0] + word1[1:], word2) + 1
            else:
                return score_function_final(word2[0] + word1, word2) + 1
        elif len(word1) > len(word2) or len(word1) >= 2 and word1[1] == word2[0]:
            return score_function_final(word1[1:], word2) + 1
        else:
            substitute_char = KEY_DISTANCES[word1[0], word2[0]] + score_function_final(word1[1:], word2[1:])
            return substitute_char
