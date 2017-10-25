
print('\n'.join(["FizzBuzz"[i*i%3*4:8-(i%5>0)*4]or"%d"%i for i in range(1,101)]))

