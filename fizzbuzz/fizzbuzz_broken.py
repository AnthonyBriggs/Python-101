
"""This is fizzbuzz, a simple Python program."""

for number in range(100):
    if number % 3 == 0 and number % 5 == 0:
        print("Fizzbuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print(Buzz)
    else:
        print(number)

ignored = input("Hit enter to continue")
