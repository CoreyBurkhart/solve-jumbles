#!/usr/bin/python

"""Finds word combinations that uses a list of letters and the length of the words in
the sentence."""

import sys
import ast

# default args
LETTERS = 'aroshoottorpme'
WORD_LENGTHS = [6, 8]

def main(letters, word_lengths):
    """encapulates program."""
    
    # Print disclaimer
    print 'Getting matches. This may take a while...'

    words = get_dictionary('/usr/share/dict/words')
    filtered = filter_by_length(words, word_lengths)
    matches = find_matches(filtered, letters)
    pretty_matches = []


    # filter duplicates and print matches all pretty-like
    for match in matches:
        if not match['remaining']:
            temp = reversed(match['matches'])
            temp = ' '.join(temp)
            if temp not in pretty_matches:
                pretty_matches.append(temp)

    for value in pretty_matches:
        print ' - ' + value


def get_dictionary(path):
    """Get all words from path as a list"""
    words = []

    # get the words and strip the newline character off the end of each
    with open(path, 'r') as words_file:
        words = map(lambda w: w[:-1], words_file.readlines())

    return words


def filter_by_length(all_words, lengths):
    """Filters a list of words based on lengths array"""
    words = {}
    for word in all_words:
        word = word.strip() # trim
        if len(word) in lengths:
            if len(word) not in words:
                words[len(word)] = []

            words[len(word)].append(word)

    return words


def test_word(word, letters, previous_words=None):
    """see if provided words can be spelled with provided letters"""
    previous_words = previous_words or []
    for letter in word:
        if letter in letters:
            letters = letters.replace(letter, '', 1)
        else:
            return False

    return {'remaining': letters, 'matches': previous_words[:] + [word]}

def test_match(match, word):
    """Alias for test_word using a match object."""
    return test_word(word, match['remaining'], match['matches'])


def find_matches(filterd_word_lists, letters):
    """asdgsa"""
    lengths = filterd_word_lists.keys()
    matches = []
    for word in filterd_word_lists[lengths[0]]:
        test = test_word(word, letters[:])
        if test != False:
            matches.append(test)

    lengths = lengths[1:]

    for length in filterd_word_lists:
        word_list = filterd_word_lists[length]
        for word in word_list:
            for match in matches:
                test = test_match(match, word)
                if test != False:
                    matches.append(test)

    return matches


if __name__ == '__main__' and len(sys.argv) == 3:
    # discard first argument (file name)
    _, LETTERS, WORD_LENGTHS = sys.argv
    # transform string from command line arg to python list
    WORD_LENGTHS = ast.literal_eval(WORD_LENGTHS)
else:
    print 'running solver with default values\nletters: {0}\nword lengths:{1}'.format(LETTERS, WORD_LENGTHS)


main(LETTERS, WORD_LENGTHS)