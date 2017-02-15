#! python

import re

from count_words import file_type, merge_histos, split_string, \
    count_words_string, walk_directory, count_words_directory, \
    count_words_zip


def test_file_type():
    assert "text/plain" == file_type("README.md")


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
          "test\\shorts\poems\\limericks\\great-britain", "test\\shorts\poems\\limericks\phoebe"]]
    ]

    for directory, excludes, soln in tests:
        files = []
        re_excludes = re.compile(excludes)
        walk_directory(directory, walk_fn=walk_fn, re_excludes=re_excludes)
        assert set(soln) == set(files)
