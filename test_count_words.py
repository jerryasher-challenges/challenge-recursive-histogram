#! python

from count_words import count_words, count_words_one, file_type, sum_histos


def test_file_type():

    assert "text/plain" == file_type("README.md")


def test_sum_histos():
    h1 = {1: 2, 3: 4}
    h2 = {1: 2, 3: 4}
    hsum = {1: 4, 3: 8}
    assert sum_histos([h1, h2]) == hsum


def test_count_words():
    assert count_words(".", None) == {}
