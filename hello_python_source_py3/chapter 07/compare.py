

class LittleNumber(object):
    def __init__(self, value):
        self.x = value
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if not (type(value) == int and 0 < value < 32):
            raise ValueError("LittleNumber.x "
                "must be an integer between 0 and 32")
        self._x = value

    def __eq__(self, other):
        return self.x == other.x
    
    def __lt__(self, other):
        return self.x < other.x
    
    def __add__(self, other):
        try:
            if type(other) == int:
                print("a")
                return LittleNumber(self.x + other)
            elif type(other) == LittleNumber:
                print("b")
                return LittleNumber(self.x + other.x)
            else:
                return NotImplemented
        except ValueError:
            raise ValueError(
                "Sum of %d and %d is out of bounds "
                "for LittleNumber!" % (self.x, other.x))
    
    def __str__(self):
        return "<LittleNumber: %d>" % self.x
    
one = LittleNumber(1)
two = LittleNumber(2)
print(one == one)
print(not one == two)
print(one != two)
print()
print(one < two)
print(two > one)
print(not one > two)
print(not two < one)
print(two >= one)
print(two >= two)

onetoo = LittleNumber(1)
print(onetoo == one)
print(not onetoo == two)
print(two > onetoo)

print(onetoo + one)
print(one)
print(onetoo + one == two)
print(LittleNumber(1) + 1)
#print LittleNumber(16) + LittleNumber(20)
print(LittleNumber(1) + "foo")
print(LittleNumber(2) - 1)