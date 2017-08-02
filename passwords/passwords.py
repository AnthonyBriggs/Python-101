
"Generate a table of random passwords for people to use"

import random
import string

# No 0Oi1lIL chars
#print(string.printable[:26*2+10])
characters = "23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ"
print(characters)


def password(digits=10):
    return ''.join(random.choice(characters) for x in range(digits))

# 20 rows of passwords
for i in range(20):
    passwords = [password() for i in range(5)]
    print("\t".join(passwords))
    print()

print("Hit enter to continue")
ignored = input()