
"""
Showing how properties work.
"""

class TestProperty(object):

    def __init__(self, x):
        self.x = x
        
    def get_x(self):
        return self._x
    
    def set_x(self, value):
        if not (type(value) == int and 0 < value < 32):
            raise ValueError("TestProperty.x "
                "must be an integer between 0 and 32")
        self._x = value
    
    #x = property(get_x, set_x)
    x = property(get_x)

test = TestProperty(10)
print(test.x)
test.x = 11
test.x += 1
assert test.x == 12
print(test.x)

#test2 = TestProperty(42)
try:
    test2 = TestProperty(42)
except ValueError:
    print("test2 not set to 42:")

    
class TestPropertyDecorator(object):
    def __init__(self, value):
        self.x = value
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if not (type(value) == int and 0 < value < 32):
            raise ValueError("TestProperty.x "
                "must be an integer between 0 and 32")
        self._x = value


test = TestPropertyDecorator(10)
print(test.x)
test.x = 11
test.x += 1
assert test.x == 12
print(test.x)

#test2 = TestPropertyDecorator(42)
try:
    test2 = TestPropertyDecorator(42)
except ValueError:
    print("test2 not set to 42:")
