# Walker

## Requirements:

An application that 

+ Allow the user to provide a path to a directory
+ Find all text files in that directory and its children
+ If it encounters a compressed archive, open it and process any text files inside
+ Output a histogram of the word counts for the files

### Questions:

+ Is a command line python program sufficient?
+ Is specifying the directory on the command line sufficient?
+ Regarding the histogram, is one histogram of the word frequencies for all of the text files sufficient?
+ What defines a text file?
    - a file name pattern ("\*.txt", "\*.text", ...)
        * what are the patterns the app should look for?
    - some other inspection of the file contents?
  + What defines a compressed archive?
    - a file name pattern ("\*.zip", "\*.tar", ".tgz", ...)
        * what are the patterns the app should look for?
    - some other inspection of the file contents?
+ Is there a preferred format of the histogram?
    - If so, can you specify that now?
    - Is json of a python dictionary suitable as output, or are you
      looking for a table, or a graph?
    
```
    histo = {'a': 1001,   
             'the' : 1200,   
             'apoplexy': 3  
            }  
```




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

