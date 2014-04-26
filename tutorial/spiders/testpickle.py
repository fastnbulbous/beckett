#import all from utilities module

from tutorial.items import BeckettItem
import pickle
import pprint
import sys

import os, fnmatch

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

# Start execution here!
if __name__ == '__main__':
    
    for path in sys.path:
        print path
    
    fileStart = "H:\\Code\\beckett\\tutorial\\Basketball"

    matches = []
    for filename in find_files("H:\\Code\\beckett\\tutorial\\Basketball", '*.pickle'):
        matches.append(filename)
        print filename

    #print file

    for match in matches:
        file = open(match, 'r')
        beckettItems = (pickle.load(file))

        for item in beckettItems:
            try:
                print "Set: " + ''.join(item['setName']) + " - Players " + ''.join(item['playerNames'])
            except:
                print "Noting"

        file.close()


