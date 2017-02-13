#!python

"""count_words.py

Walks a directory. Finds all text files in that directory and it's
children, creating a histogram of the word counts for the files.

Along the way it opens compressed archives and processes any text
files inside.

Output: a histogram of the word counts for the files.

Usage: count_words.py
  count_words.py [<directory>] [options] [-v...]
  count_words.py -h | --help

Options:
--test                      print basic args, do nothing else.
-x <dirs> --exclude <dirs>  comma separated directory pattern to exclude [default: .git]      
-v --verbose                print verbose status messages
-h --help                   Show this screen

If no directory is specified, count_words defaults to the current directory

"""

import fnmatch
import os
import re
import subprocess

from docopt import docopt


def sum_histos(histo_list):
    """adds the word counts of a list of histogram into a new"""
    histo = {}
    for h in histo_list:
        for k, v in h.items():
            if k in histo:
                histo[k] = histo[k] + v
            else:
                histo[k] = v
    return histo


def file_type(file):
    """return the file type of a file
    requires the file command, which is built in to linux and mac
    and can be installed from cygwin on windows"""

    result = subprocess.check_output("file --mime-type {}".format(file))
    result = result.decode("utf-8")
    mime_type = result.split()[-1]
    return mime_type


def count_words_one(path):
    """count the words in one item (may be file or compressed archive)"""
    return {}


def count_words(directory, re_excludes=None):
    """walk a directory, returning a histogram of word counts in the files"""

    if not re_excludes:
        re_excludes = re.compile(r"^/:/")  # illegal linux and win filename

    h = []
    for dirpath, dirs, files in os.walk(directory):
        print("dirpath: %s" % dirpath)
        print("dirs: %s" % dirs)
        print("files: %s" % files)
        print("")

        for f in files:
            if not re.search(re_excludes, f):
                path = os.path.join(dirpath, f)
                h.append(count_words_one(path))
        dirs[:] = [d for d in dirs if not re.search(re_excludes, d)]

    histo = sum_histos(h)

    return histo


if __name__ == "__main__":

    args = docopt(__doc__)
    verbose = args['--verbose']

    directory = args['<directory>']
    if not directory:
        directory = "."

    excludes = args['--exclude']
    excludes = excludes.split(",")
    re_excludes = re.compile("(" + ")|(".join(excludes) + ")")

    if args['--test']:
        print(args)
        print("directory is %s" % directory)
        print("excludes is %s" % excludes)
        exit()

    if verbose > 1:
        print(args)

    print(count_words(directory, re.excludes))
