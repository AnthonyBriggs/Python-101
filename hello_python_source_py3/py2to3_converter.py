
"""Script to mass-convert all the Python 2 files in a directory to Python 3."""

import os
import sys

try:
    target = sys.argv[1]
    if target.endswith('"'):
        target = target[:-1]
except IndexError:
    target = "."

print(target)
#sys.exit(1)    # debug

for path, dirs, files in os.walk(target):
    print(path, files, dirs)
    for file_name in files:
        print(file_name)
        if not file_name.endswith('.py'):
            continue
        file_path = os.path.join(path, file_name)
        print("Converting ", file_path)
        #print("python -m lib2to3 -wn '" + file_path + "'")
        # Double quotes are for Windows systems, which don't like 
        # file arguments with spaces :P
        os.system('python -m lib2to3 -wn "' + file_path + '"')
