#!/usr/bin/env python3

"""
Generates random "passwords" from wordlists.

This is a _very basic_ attempt to generate passwords inspired by this:
<https://xkcd.com/936/>.

This script is at home at: <https://github.com/brutus/horsebat>

"""

import sys
import argparse

from random import randint

from slugify import slugify


__version__ = '0.0.0'

DEFAULT_WORDFILE = '/usr/share/dict/words'

DESCRIPTION = (
    "Loads random words from a source file (one word per line), "
    "slugifies each, maybe changes the case and glues them together."
)


def parse_args(argv=None):
    """
    Returns a namespace containing the parsed arguments from *argv*.

    """
    ap = argparse.ArgumentParser(
        description=DESCRIPTION,
    )
    # arguments
    ap.add_argument(
      'filename', nargs='?',
      help="load words from this file (%(default)s)"
    )
    # options
    ap.add_argument(
      '--version', action='version', version=__version__,
      help="prints version and exits"
    )
    # word cleanup
    g_cleanup = ap.add_argument_group('Word Cleanup')
    g_cleanup.add_argument(
      '-c', '--case', choices=('upper', 'lower', 'title', 'unchanged'),
      help="convert words to upper/lower/title case (%(default)s)"
    )
    g_cleanup.add_argument(
      '-C', '--first-case', choices=('upper', 'lower', 'unchanged'),
      help="covert 1st char to upper/lower case (%(default)s)"
    )
    g_cleanup.add_argument(
      '-s', '--separator', metavar='SEPERATOR',
      help="seperate cleaned words with this ('%(default)s')"
    )
    g_cleanup.add_argument(
      '-S', '--slug-separator', metavar='SEPERATOR',
      help="separator for slugify ('%(default)s')"
    )
    # selection
    g_select = ap.add_argument_group('Word Selection')
    g_select.add_argument(
      '-m', '--min-length', type=int,
      help="word need to be at least this long ('%(default)s')"
    )
    g_select.add_argument(
      '-M', '--max-length', type=int,
      help="word can be only this long ('%(default)s')"
    )
    g_select.add_argument(
      '-r', '--no-random', action='store_false', dest='random',
      help="don't select words at random"
    )
    g_select.add_argument(
      '-u', '--no-unique', action='store_false', dest='unique',
      help="might use the same worde more than once"
    )
    g_select.add_argument(
      '-w', '--word-count', type=int, dest='count',
      help="glue this many words together ('%(default)s')"
    )
    # defaults
    ap.set_defaults(
        filename=DEFAULT_WORDFILE,
        case='title',
        first_case='lower',
        separator='',
        slug_separator='',
        min_length=4,
        max_length=12,
        random=True,
        unique=True,
        count=4,
    )
    # return args
    args = ap.parse_args(argv)
    return args


def load_wordlist(filename=DEFAULT_WORDFILE):
    """
    Returns a list of words from *filename*.

    The file should contain one word per line.

    """
    with open(filename) as fh:
        lines = [line.strip() for line in fh]
    return lines


def clean_word(word, case=None, separator=''):
    """
    Returns a cleaned (slugified) version of *word*.

    If *case* is `True`, the cleaned result is converted to tilte case, or to
    lower case, if *case* is set to `False`. Otherwise it is left untouched.

    """
    cleaned_word = slugify(word, separator=separator)
    if case == 'lower':
        cleaned_word = cleaned_word.lower()
    elif case == 'upper':
        cleaned_word = cleaned_word.upper()
    elif case == 'title':
        cleaned_word = cleaned_word.title()
    return cleaned_word


def check_word(word, min_length=4, max_length=12):
    """
    Retruns `True` if the word fits in the rules, `Fale` otherwise.

    """
    word_length = len(word)
    if min_length and word_length < min_length:
        return False
    if max_length and word_length > max_length:
        return False
    return True


def wordssource(
    wordlist, random=True, unique=True, min_length=4, max_length=12,
    case=None, separator=''
):
    """
    Yields cleaned up words from *filename*.

    """
    wordlist = wordlist.copy()
    yielded_words = set()
    while wordlist:
        idx = randint(0, len(wordlist) - 1) if random else 0
        word = wordlist.pop(idx)
        word = clean_word(word, case, separator)
        if not check_word(word, min_length, max_length):
            continue
        if unique and word in yielded_words:
            continue
        yielded_words.add(word)
        yield word


def get_password(source, count, separator='', case=None):
    """
    Returns *wordcount* words from *source* joined with *separator*.

    If *case* is set to `upper` or `lower` the case of the first char
    is cast to uppper or lower case.

    """
    tokens = [next(source) for x in range(count)]
    word = separator.join(tokens)
    if case == 'lower':
        word = word[0].lower() + word[1:]
    elif case == 'upper':
        word = word[0].upper() + word[1:]
    return word


def main(argv=None):
    """
    Parses *argv* (default = commandline) and prints to STDOUT.

    """
    args = parse_args(argv)
    wordsource = wordssource(
        load_wordlist(args.filename),
        args.random, args.unique, args.min_length,
        args.max_length, args.case, args.slug_separator
    )
    word = get_password(
        wordsource, args.count, args.separator, args.first_case
    )
    print(word)
    return 0


if __name__ == '__main__':
    sys.exit(main())
