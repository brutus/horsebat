# HorseBat

A _very basic_ attempt to generate passwords inspired by this:
<https://xkcd.com/936/>.


## Example

```
$ ./horsebat.py
chainsawingJackalOnlookerTucking
```

```
$ ./horsebat.py -w 3 -s- -c lower
worthiest-staunched-alba
```


## Usage

```
usage: horsebat.py [-h] [--version] [-c {upper,lower,title,unchanged}]
                   [-C {upper,lower,unchanged}] [-s SEPERATOR] [-S SEPERATOR]
                   [-m MIN_LENGTH] [-M MAX_LENGTH] [-r] [-u] [-w COUNT]
                   [filename]

Loads random words from a source file (one word per line), slugifies each,
maybe changes the case and glues them together.

positional arguments:
  filename              load words from this file (/usr/share/dict/words)

optional arguments:
  -h, --help            show this help message and exit
  --version             prints version and exits

Word Cleanup:
  -c {upper,lower,title,unchanged}, --case {upper,lower,title,unchanged}
                        convert words to upper/lower/title case (title)
  -C {upper,lower,unchanged}, --first-case {upper,lower,unchanged}
                        covert 1st char to upper/lower case (lower)
  -s SEPERATOR, --separator SEPERATOR
                        seperate cleaned words with this ('')
  -S SEPERATOR, --slug-separator SEPERATOR
                        separator for slugify ('')

Word Selection:
  -m MIN_LENGTH, --min-length MIN_LENGTH
                        word need to be at least this long (4)
  -M MAX_LENGTH, --max-length MAX_LENGTH
                        word can be only this long (12)
  -r, --no-random       don't select words at random
  -u, --no-unique       might use the same worde more than once
  -w COUNT, --word-count COUNT
                        glue this many words together (4)
```
