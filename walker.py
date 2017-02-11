#!python

"""walker.py

Walks a directory.

Finds all text files in that directory and it's children, creating a
histogram of the word counts for the files.

Along the way it opens compressed archives and processes any text
files inside.

Output: a histogram of the word counts for the files.

Usage: walker.py
  walker.py [<directory>] [options] [-v...]
  walker.py -h | --help

Options:
-v --verbose                print verbose status messages
-h --help                   Show this screen

If no directory is specified, walker defaults to the current directory

"""

from docopt import docopt


def walker(directory):
    return None


if __name__ == "__main__":

    args = docopt(__doc__)
    verbose = args['--verbose']

    print(args)

    if verbose > 1:
        print(args)

    directory = args['<directory>']

    print(walker(directory))
