from pathlib import Path
from collections import defaultdict, namedtuple
from operator import attrgetter
from pprint import pprint


wwf_value = namedtuple("wwf_value", "word value wildcards length")
p = Path.cwd()
dictionary_file = p / 'dictionary.txt'
wwf_eval = {}


words_with_friends_scores = (
    (1, "A E I O R S T"),
    (2, "D L N U"),
    (3, "G H Y"),
    (4, "B C F M P W"),
    (5, "K V"),
    (8, "X"),
    (10, "J Q Z"),
)


LETTER_SCORES = {letter: score for score, letters in words_with_friends_scores
                 for letter in letters.split()}

LETTER_TILES = {
    'A': 9, 'B': 2, 'C': 2, 'D': 5, 'E': 13,
    'F': 2, 'G': 3, 'H': 4, 'I': 8, 'J': 1,
    'K': 1, 'L': 4, 'M': 2, 'N': 5, 'O': 8,
    'P': 2, 'Q': 1, 'R': 6, 'S': 5, 'T': 7,
    'U': 4, 'V': 2, 'W': 2, 'X': 1, 'Y': 2,
    'Z': 1,
    '*': 2  # Wildcard titles no value
}


def word_value(word=None):
    """Determine the Words with Friends value and wildcard totals."""
    if word is None:
        return 0
    letters_used = defaultdict(int)
    value = 0
    wild_cards_needed = 0
    for letter in word:
        letters_used[letter] += 1
    for letter, letter_count in letters_used.items():
        value += min(letter_count, LETTER_TILES[letter]) \
            * LETTER_SCORES[letter]
        if letter_count > LETTER_TILES[letter]:
            wild_cards_needed += letter_count - LETTER_TILES[letter]
    if wild_cards_needed > 2:  # At most there can only be 2 wildcards
        return wwf_value(word, 0, 0, 0,)
    return wwf_value(word, value, wild_cards_needed, len(word),)


def valid_word(word=None):
    """Validate if word is valid in Words with Friends."""
    if any([l is '-' for l in word]):
        return None
    if len(word) < 2:
        return None
    return word


def main():
    """Find the best possible scores.

    Using a dictionary text file, return all the best scores.
    """
    with open(dictionary_file, 'r') as f:
        for line in f:
            word = line.strip().upper()
            word = valid_word(word)
            if word:
                wwf_eval[word] = word_value(word)
    pprint([(k, wwf_eval[k],)
            for k in sorted(wwf_eval,
                            key=lambda x: (wwf_eval[x].value, wwf_eval[x].length),
                            reverse=True
                            )])


if __name__ == "__main__":
    main()
