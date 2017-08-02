#!/usr/bin/env python3

import random

print ("Random multiplication problems".center(80))
print ("------------------------------".center(80))
print ("")

first_digits = "123456789"
digits = "0123456789"

def random_number(number_digits):
    number = random.choice(first_digits)
    for i in range(number_digits - 1):
        number = number + random.choice(digits)
    return int(number)

def make_mult_problem(num1_digits, num2_digits):
    return [random_number(num1_digits),
            random_number(num2_digits)]


"""
print (random_number(2))
print (random_number(3))
print (random_number(4))
print (random_number(10))

print (random_number(2) + random_number(2))
print ("----------")

print (make_mult_problem(3, 2))
print (make_mult_problem(4, 3))
"""

"""
Layout:

  4410              4410                4410
x  167            x  167              x  167

  4410              4410                4410
x  167            x  167              x  167

  4410              4410                4410
x  167            x  167              x  167

  4410              4410                4410
x  167            x  167              x  167

  4410              4410                4410
x  167            x  167              x  167
"""

rows = 10
columns = 3
space_per_col = 80 // 3

# testing column spacing
"""print (str(space_per_col))
for i in range(40):
    print (str(space_per_col).rjust(space_per_col) +
        str(space_per_col).rjust(space_per_col) +
        str(space_per_col).rjust(space_per_col))
"""

for row in range(rows):
    problem_row = []
    for column in range(columns):
        # TODO: random problem between 3,2  4,3 and 4, 2
        harditude = random.choice([(3,2), (4,3), (4,2)])
        problem_row.append( make_mult_problem(*harditude) )
    #print (problem_row)
    
    row1 = ""
    row2 = ""
    for problem in problem_row:
        row1 += str(problem[0]).rjust(space_per_col)
        row2 += ("x " + str(problem[1])).rjust(space_per_col)
    print (row1)
    print (row2)
    print ("\n"*5)
    
