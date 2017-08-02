import logging

"""
A script to test the behaviour of Python's super() function
with diamond inheritance.
"""

class A(object):
    def __init__(self):
        print("initing class A!")
        
class B(A):
    def __init__(self):
        print("initing class B!")
        if direct[1]:
            A.__init__(self)
        else:
            super(B, self).__init__()

class C(A):
    def __init__(self):
        print("initing class C!")
        if direct[2]:
            A.__init__(self)
        else:
            super(C, self).__init__()

class MyClass(C, B):
    """A class that you write."""
    
    def __init__(self):
        if direct[0]:
            C.__init__(self)
            B.__init__(self)
        else:
            super(MyClass, self).__init__()
            
    def do_something(self):
        print("Doing something!")
        print()


# This will call A's __init__ function twice
direct = (True, True, True)
test = MyClass()
test.do_something()

# This will call too many init functions
direct = (True, False, False)
test2 = MyClass()
test2.do_something()

# This won't call B's init function
direct = (False, True, True)
test3 = MyClass()
test3.do_something()

# Straight inheritance works fine with direct calls,
# since there's no diamond inheritance
direct = (True, True, True)
test4 = C()

# You need direct to be all False,
# ie. super() everywhere
direct = (False, False, False)
test4 = MyClass()
test4.do_something()

