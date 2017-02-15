#! python

import re

from count_words import file_type, merge_histos, split_string, \
    count_words_string, walk_directory, count_words_directory, \
    walk_zip, count_words_zip


def test_file_type():
    assert "text/plain" == file_type("README.md")
    assert "application/zip" == file_type("test/shorts.zip")


def test_merge_histos():
    h1 = {1: 2, 3: 4}
    h2 = {1: 2, 3: 4}
    hmerge = {1: 4, 3: 8}
    assert merge_histos([h1, h2]) == hmerge


def test_split_string():
    tests = [
        ["""abc,def""", ["abc", "def"]],
        ["""""", []],
        ["""abc87432387##$#def""", ["abc", "def"]],
        ["Words, words, words.", ["Words", "words", "words"]],
    ]
    for test, soln in tests:
        assert soln == split_string(test)


def test_count_words_string():
    tests = [
        ["abc, 'def' /ghi\ abc+;- def ABC DeF ABC", {
            'abc': 4,
            'def': 3,
            'ghi': 1
        }]
    ]
    for test, soln in tests:
        assert soln == count_words_string(test)


def test_walk_directory():
    files = []

    def walk_fn(path, *_):
        files.append(path)

    tests = [
        ["test", r"[.]",
         ["test\\preamble",
          "test\\roybatty",
          "test\\maelstrom\\ahab",
          "test\\shorts\poems\\jabberwocky",
          "test\\shorts\poems\\limericks\\a-flea", "test\\shorts\poems\\limericks\\a-mouse",
          "test\\shorts\poems\\limericks\\great-britain", "test\\shorts\poems\\limericks\phoebe",
          "test\\twozip\\2ndLevel\\tomorrow",
          ]]
    ]

    for directory, excludes, soln in tests:
        files = []
        re_excludes = re.compile(excludes)
        walk_directory(directory, walk_fn=walk_fn, re_excludes=re_excludes)
        assert set(soln) == set(files)


def test_walk_zip():

    files = []

    def walk_fn(path, *_):
        files.append(path)

    tests = [["test/onezip.zip", r"[.]", []],
             ["test/twozip.zip", r"[.]", ["twozip/2ndLevel/tomorrow"]],
             ]

    for path, excludes, soln in tests:
        files = []
        re_excludes = re.compile(excludes)
        walk_zip(path, walk_fn=walk_fn, re_excludes=re_excludes)
        assert set(soln) == set(files)


def test_count_words_zip():

    files = []

    def walk_fn(path, *_):
        files.append(path)

    tests = [["test/onezip.zip", r"[.]", {}],
             ["test/twozip.zip", r"[.]", {
                 'any': 1, 'anything': 3, 'are': 2,
                 'busy': 1, 'cards': 1, 'doing': 2,
                 'for': 4, 'got': 3, 'happening': 1,
                 'have': 2, 'how': 1, 'looking': 1,
                 'on': 2, 'plan': 1, 'planned': 1,
                 'plans': 1, 's': 4, 'the': 1,
                 'tomorrow': 10, 'what': 4, 'you': 4,
                 'your': 1
             }]]

    for path, excludes, soln in tests:
        files = []
        re_excludes = re.compile(excludes)
        h = count_words_zip(path, re_excludes=re_excludes)
        assert soln == h


def test_count_words_directory():
    zip_histo = count_words_zip("test/shorts.zip", re_excludes=":/")
    dir_histo = count_words_directory("test/shorts", re_excludes=":/")
    assert(zip_histo == dir_histo)
