
import random
import string
from textwrap import wrap

sysrandom = random.SystemRandom()


def print_table(tabula):
    output = []
    y_max = max(set([coords[1] for coords in tabula.keys()]))
    x_max = max(set([coords[0] for coords in tabula.keys()]))
    
    for y in range(y_max+1):
        line = []
        for x in range(x_max+1):
            if tabula[(x,y)] == "-" and y == 1:
                line.append("--")
            else:
                line.append(tabula[(x,y)]+" ")
        output.append("".join(line))
    
    return output

def y_indexer():
    y = list(reversed(v_indexes[2:]))
    while 1:
        n = y.pop()
        if n == " ":
            continue
        if n in "*-.":
            yield " "
        else:
            yield n

h_indexes = "*-..ABCDEFGHIJKLM NOPQRSTUVWXYZ.."
v_indexes = "*-..ABCDEFGH  IJKLMNOPQR  STUVWXYZ.."

# replace characters which are easily misread
characters = (string.printable[:-6]
                    .replace("l", "").replace("I", "")
                    .replace("O", "")
                    .replace("{", "").replace("}", "")
                    .replace("|", ""))
tabula = {}              

y_index = y_indexer()
#print dir(y_indexer)

for YI, Y in enumerate(v_indexes):
    if Y == " " or Y == "-":
        # horizontal axis line at the top,
        # or spacing in the middle
        for XI, X in enumerate(h_indexes):
            if XI == 0:
                tabula[(XI, YI)] = " "
            elif X == "-" and Y == "-":
                tabula[(XI, YI)] = "+"
            elif X == "-":
                tabula[(XI, YI)] = "|"
            else:
                tabula[(XI, YI)] = Y  # either " " or "-"
    
    elif Y == "*":
        # horizontal axis letters
        for XI, X in enumerate(h_indexes):
            if XI == 1:
                tabula[(XI, YI)] = " "
            elif X == "-":
                tabula[(XI, YI)] = "|"
            elif X in " *.":
                tabula[(XI, YI)] = " "
            else:
                tabula[(XI, YI)] = X

    else:
        # Y-lettered axis row
        for XI, X in enumerate(h_indexes):
            if X == "*":
                tabula[(XI, YI)] = next(y_index)
            elif X == " ":
                tabula[(XI, YI)] = " "
            elif X == "-":
                tabula[(XI, YI)] = "|"
            else:
                tabula[(XI, YI)] = sysrandom.choice(characters)


output = print_table(tabula)

output.append("""

Chosen randomly from:""")
for line in wrap(characters, width=50):
    output.append(line)

output.append("""

Based on a blog post from John Graham-Cumming:
   blog.jgc.org/2010/12/write-your-passwords-down.html
""")

print("\n".join(output))

# TESTING *ONLY* - cut+paste+print it out, don't save to your hard drive!!1!
#open('password_tabula.txt', 'w').write("\n".join(output))

delay = input("Hit enter to continue")

