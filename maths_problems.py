#!/usr/bin/python

"""
A quick script to generate maths problems.
BIMDAS, etc.
"""

import random
import sys


class Level(object):
    def __init__(self, min_number, max_number, min_count, max_count, terms):
        self.min_number = min_number
        self.max_number = max_number
        self.min_count = min_count
        self.max_count = max_count
        self.terms = terms

    def number(self):
        """Pick a random number in our range."""
        return random.randint(self.min_number, self.max_number)

    def count(self):
        """Pick a random count of numbers."""
        return random.randint(self.min_count, self.max_count) - 1

    def term(self):
        """Pick a random term."""
        return random.choice(self.terms)

    def problem(self):
        """Return a problem from this level."""
        result = [self.number()]
        for i in range(self.count()):
            term = self.term()
            result.append(term)
            if term == '/':
                # make division slightly less hard
                result.append(int(self.number() / 10.0))
            else:
                result.append(self.number())
        problem = ' '.join(str(r) for r in result)
        return (problem, eval(problem))


# Create the problem levels
levels = [
    Level(0, 10, 2, 2, ('+',)),
    Level(0, 10, 2, 2, ('+', '-')),
    Level(0, 20, 2, 2, ('+', '-')),
    Level(0, 20, 2, 2, ('+', '-')),
    Level(0, 10, 2, 2, ('+', '-', '*')),
    Level(0, 20, 2, 2, ('+', '-', '*')),
    Level(10, 50, 2, 2, ('+', '-', '*')),
    Level(20, 100, 2, 2, ('+', '-', '*')),
    Level(20, 100, 2, 3, ('+', '-', '*')),
    Level(10, 50, 2, 2, ('+', '-', '*', '/')),
    Level(20, 100, 2, 3, ('+', '-', '*', '/')),
    Level(50, 250, 2, 2, ('+', '-')),
    Level(50, 250, 2, 2, ('+', '-', '*')),
    Level(50, 250, 2, 3, ('+', '-', '*')),
    Level(100, 500, 2, 3, ('+', '-',)),
    Level(50, 250, 2, 2, ('+', '-', '*', '/')),
    Level(50, 250, 2, 3, ('+', '-', '*', '/')),
    Level(100, 500, 2, 3, ('+', '-', '*')),
    Level(100, 500, 2, 3, ('+', '-', '*', '/')),
    Level(250, 1000, 2, 3, ('+', '-', '*')),
    Level(250, 1000, 2, 4, ('+', '-', '*'))
]

# make sure the levels know what level they are...
for index, level in enumerate(levels):
    levels[index].level = index + 1

if __name__ == '__main__':
    # pick a start and end level, if we're given them
    if len(sys.argv) == 3:
        start_level = int(sys.argv[1])
        end_level = int(sys.argv[2])
    else:
        start_level = 1
        end_level = 5

    # Now build a list of problems
    problems = []
    for i in range(25):
        level = random.randint(start_level, end_level)
        problem_text, solution = levels[level].problem()
        problems.append([level, problem_text, solution])
    
    # put the problems in order - low to high level
    problems.sort()
    
    # print the questions
    for index, (level, problem_text, solution) in enumerate(problems):
        print ("%2d (level %2d). \t%s = ?" % (index+1, level, problem_text))
    
    print ("-" * 42)
    
    # print the solutions
    for index, (level, problem_text, solution) in enumerate(problems):
        print ("%2d (level %2d). \t%s = %s" % (index+1, level, problem_text, solution))


