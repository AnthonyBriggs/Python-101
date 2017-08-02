
"""
An example of using __getattr__ and __setattr__
"""

class TestGetAttr(object):
    
    def __getattr__(self, name):
        print("Attribute '%s' not found!" % name)
        return 42

test_class = TestGetAttr()
print(test_class.something)

test_class.something = 43
print(test_class.something)


class TestSetAttr(object):

    def __init__(self):
        self.__dict__['things'] = {}
        
    def __setattr__(self, name, value):
        print("Setting '%s' to '%s'" % (name, value))
        self.things[name] = value
    
    def __getattr__(self, name):
        try:
            return self.things[name]
        except KeyError:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % 
                    (self.__class__.__name__, name))

test_class2 = TestSetAttr()
test_class2.something = 42
print(test_class2.something)
print(test_class2.things)
#print test_class2.something_else


def get_real_attr(instance, name):
    return object.__getattribute__(instance, name)
    
class TestGetAttribute(object):
    
    def __init__(self, things=None):
        my_dict = get_real_attr(self, '__dict__')
        if not things:
            my_dict['things'] = {}
        else:
            my_dict['things'] = things
            
    def __setattr__(self, name, value):
        print("Setting '%s' to '%s'" % (name, value))
        my_dict = get_real_attr(self, '__dict__')
        my_dict['things'][name] = value

    def __getattribute__(self, name):
        try:
            my_dict = get_real_attr(self, '__dict__')
            return my_dict['things'][name]
        except KeyError:
            my_class = get_real_attr(self, '__class__')
            raise AttributeError(
                "'%s' object has no attribute '%s'" % 
                    (my_class.__name__, name))
        
test_class3 = TestGetAttribute({'foo': 'bar'})
print(object.__getattribute__(test_class3, '__dict__'))
test_class3.something = 43
print(object.__getattribute__(test_class3, '__dict__'))
print(test_class3.foo)

