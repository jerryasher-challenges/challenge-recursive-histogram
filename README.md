# Recursive histogram

## Requirements:

Create an application:

+ Allow the user to provide a path to a directory
+ Find all text files in that directory and its children
+ If it encounters a compressed archive, open it and process any text files inside
+ Output a histogram of the word counts for the files

## Usage:

    Usage: walker.py
      walker.py [<directory>] [options] [-v...]
      walker.py -h | --help

    Options:
    -v --verbose                print verbose status messages
    -h --help                   Show this screen

    If no directory is specified, walker defaults to the current directory

## Testing:

This application supports pytest. To run self tests, use

    $ pytest

