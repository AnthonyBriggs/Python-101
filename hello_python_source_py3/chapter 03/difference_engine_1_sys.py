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
