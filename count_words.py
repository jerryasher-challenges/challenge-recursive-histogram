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
-x <pattern> --exclude <pattern>  exclude files and directories that
                            match this comma separated regex
                            [default: .git,~$,__$,#$,#.*$,^\.]
-v --verbose                print verbose status messages
-h --help                   Show this screen

If no directory is specified, count_words defaults to the current directory

"""

from docopt import docopt
import os
import subprocess
import re
from zipfile import ZipFile


def file_type(file):
    """return the file type of a file
    requires the file command, which is built in to linux and mac
    and can be installed from cygwin on windows"""

    result = subprocess.check_output("file --mime-type {}".format(file))
    result = result.decode("utf-8")
    mime_type = result.split()[-1]
    return mime_type


def split_string(s):
    """splits a string into it's component words"""
    words = re.findall('[A-Za-z]+', s)
    return words


def merge_histos(histo_list):
    """merges the word counts of a list of histogram into new"""
    histo = {}
    for h in histo_list:
        for k, v in h.items():
            if k in histo:
                histo[k] = histo[k] + v
            else:
                histo[k] = v
    return histo


def count_words_string(a_string, verbose=0):
    """returns a histo (dict) of the counted words, words are all downcased."""

    word_list = split_string(a_string)

    histo = {}
    for word in word_list:
        word = word.lower()
        if word in histo:
            histo[word] += 1
        else:
            histo[word] = 1
    return histo


def walk_zip(zip_path, walk_fn=None, re_excludes=None, verbose=0):
    """walk a zipfile, calling walk_fn for each file found, skips
    directories and files that match the re_excludes re."""

    with ZipFile(zip_path, "r") as z:
        entries = z.namelist()

        for entry in entries:
            if not entry.endswith("/"):
                if not re.search(re_excludes, entry):

                    if walk_fn:
                        with z.open(entry) as f:
                            whole_string = f.read().decode("utf-8")

                            walk_fn(entry, whole_string, re_excludes, verbose)
                    if verbose:
                        print(zip_path)
                else:
                    if verbose > 1:
                        print("%s excluded" % f)


def count_words_zip(path, re_excludes=None, verbose=0):
    """walk a zip file, returning a histo of word counts in the files"""

    h = []

    def count_string(entry, whole_string, re_excludes, verbose):
        histo = count_words_string(whole_string, verbose)
        if verbose > 2:
            print("walk_fn: histo is {}".format(histo))
        h.append(histo)

    walk_zip(path, walk_fn=count_string,
             re_excludes=re_excludes, verbose=verbose)

    histo = merge_histos(h)
    return histo


def count_words_item(path, re_excludes=None, verbose=0):
    """count the words in one item (may be file or compressed archive)"""

    filetype = file_type(path)
    if verbose > 2:
        print("{} -> {}".format(filetype, path))
    histo = {}
    if filetype == "text/plain":
        with open(path, "r", encoding="UTF-8") as f:
            whole_file = f.read()
        histo = count_words_string(whole_file, verbose)
    elif filetype in ["application/zip", "application/java-archive"]:
        histo = count_words_zip(path, re_excludes, verbose)

    if verbose > 2 and histo != {}:
        print(histo)

    return histo


def walk_directory(directory, walk_fn=None, re_excludes=None, verbose=0):
    """walk a directory, calling walk_fn for each file found, skips
    directories and files that match the re_excludes re."""

    for dirpath, dirs, files in os.walk(directory):
        if verbose:
            print("")
            print("dirpath: {}".format(dirpath))
            print("dirs: {}".format(dirs))
            print("files: {}".format(files))
            print("")

        for f in files:
            if not re.search(re_excludes, f):
                path = os.path.join(dirpath, f)
                if walk_fn:
                    walk_fn(path, re_excludes, verbose)
                if verbose:
                    print(path)
            else:
                if verbose > 1:
                    print("%s excluded" % f)

        if re_excludes:
            dirs[:] = [d for d in dirs if not re.search(re_excludes, d)]


def count_words_directory(directory, re_excludes=None, verbose=0):
    """walk a directory, returning a histogram of word counts in the files"""

    h = []

    def count_file(path, re_excludes, verbose):
        histo = count_words_item(path, re_excludes, verbose)
        if verbose > 2:
            print("walk_fn: histo is {}".format(histo))
        h.append(histo)

    walk_directory(directory, walk_fn=count_file,
                   re_excludes=re_excludes, verbose=verbose)

    histo = merge_histos(h)
    return histo


def print_histo(histo):

    total = 0
    max_word_len = 0
    for k in histo:
        if len(k) > max_word_len:
            max_word_len = len(k)
        total += histo[k]

    sorted_histo = sorted(
        histo.items(), key=lambda item: item[1], reverse=True)

    for word, count in sorted_histo:
        percent = int(100 * count / total)
        if percent <= 0:
            break
        print("{:>{width}}: {}".format(
            word, '*' * percent, width=max_word_len))


if __name__ == "__main__":

    args = docopt(__doc__)
    verbose = args['--verbose']

    directory = args['<directory>']
    if not directory:
        directory = "."

    excludes = args['--exclude']
    excludes = excludes.split(",")
    re_excludes = re.compile("(" + ")|(".join(excludes) + ")")

    if verbose:
        print(args)
    if verbose > 2:
        print("directory is {}".format(directory))
        print("excludes is {}".format(excludes))

    histo = count_words_directory(directory, re_excludes, verbose)

    print_histo(histo)
