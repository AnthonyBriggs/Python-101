
import hashlib
import os
import sys

if len(sys.argv) < 3:                                    #1
    print("You need to specify two directories:")        #1
    print(sys.argv[0], "<directory 1> <directory 2>")    #1
    sys.exit()                                          #1
directory1 = sys.argv[1]                                 #2
directory2 = sys.argv[2]                                 #2
print("Comparing:")
print(directory1)
print(directory2)

for directory in [directory1, directory2]:
    if not os.access(directory, os.F_OK):
        print(directory, "is not a valid directory!")
        sys.exit()

def md5(file_path):
    read_file = open(file_path, "rb")
    the_hash = hashlib.md5()
    for line in read_file.readlines():
        the_hash.update(line)
    return the_hash.hexdigest()

def directory_listing(directory_name):
    dir_file_list = {}
    dir_root = None
    dir_trim = 0
    for path, dirs, files in os.walk(directory_name):
        if dir_root is None:
            dir_root = path
            dir_trim = len(dir_root)
            print("dir", directory_name, end=' ')
            print("root is", dir_root)
        trimmed_path = path[dir_trim:]
        if trimmed_path.startswith(os.path.sep):
            trimmed_path = trimmed_path[1:]
        #print "path is", path, " and trimmed_path is", trimmed_path
        for each_file in files:
            file_path = os.path.join(trimmed_path, each_file)
            dir_file_list[file_path] = True
    return (dir_file_list, dir_root)

dir1_file_list, dir1_root = directory_listing(directory1)
dir2_file_list, dir2_root = directory_listing(directory2)
results = {}

for file_path in list(dir2_file_list.keys()):
    if file_path not in dir1_file_list:
        results[file_path] = "not found in directory 1"
    else:
        #print file_path, "found in directory 1 and 2"
        file1 = os.path.join(dir1_root, file_path)
        file2 = os.path.join(dir2_root, file_path)
        if md5(file1) != md5(file2):
            results[file_path] = "is different in directory 2"
        else:
            results[file_path] = "is the same in both"

for file_path, value in list(dir1_file_list.items()):
    if file_path not in results:
        results[file_path] = "not found in directory 2"

print()
for path, result in sorted(results.items()):
    if os.path.sep not in path and "same" not in result:
        print(path, result)

for path, result in sorted(results.items()):
    if os.path.sep in path and "same" not in result:
        print(path, result)
