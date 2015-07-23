"""

fake_enums.py

A really dumb way to implement fake enums in Python.

"""

import sys
from new import classobj
from functools import partial

__all__ = (
    'FakeEnum',
    'fake_enum',
)


class FakeEnum(object):
    """ Base class for the fake enum type. """
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __repr__(self):
        return "{}({}, {})".format(
                self.__class__.__name__,
                repr(self.name),
                repr(self.value),
            )
            
    def __str__(self):
        return self.name
        
    def __int__(self):
        return self.value
        
    def __eq__(self, other):
        return self.name == other.name and self.value == other.value
        
    def __ne__(self, other):
        return not self == other
        
        
def fake_enum(arg, _initial=0):
    """ Takes a class and returns an evil version of that class, with 
    everything defined inside that class's 'value' tuple converted into actual
    enum values as class attributes, which themselves are instances of that 
    class.
    
    Also makes the class iterable over its defined enum values, because WHY 
    THE HELL NOT.
    
    If the argument is an integer, returns a new version of the fake_enum
    decorator that can be used to create enums that start from the given 
    number.
    
    """
    
    if isinstance(arg, type) or isinstance(arg, classobj):
        Decorated = arg
        
        # Wow so meta such hack
        class __metaclass__(type):
            def __iter__(self):
                # Hooray abuse of Python's ridiculous closure behavior!
                return iter(values)
                
        # Hack hack hackity hack
        FakeEnumType = __metaclass__(
                Decorated.__name__,
                (FakeEnum,),
                {'__doc__' : Decorated.__doc__},
            )
            
        values = []
        for i, value in enumerate(Decorated.values):
            if isinstance(value, basestring):
                valueName = value
                valueNum = _initial + i
            else:
                try:
                    valueName, valueNum = value
                except ValueError:
                    raise TypeError(
                            "'value' elements must be either a "
                            "string or a collection of length 2."
                        )
                        
            fakeEnumValue = FakeEnumType(valueName, valueNum)
            
            # Hack erry day
            setattr(FakeEnumType, valueName, fakeEnumValue)
            
            values.append(fakeEnumValue)
            
        return FakeEnumType
        
    elif isinstance(arg, int):
        return partial(fake_enum, _initial=arg)
        
    else:
        assert False
        
        
##################################################################
# Informal quick and stupid test case goes here because I'm lazy #
##################################################################

def _test():
    
    @fake_enum(100)
    class Blag:
        """ A fake enum type. """
        
        values = (
            'FOO',
            'BAR',
            'BIZ',
            'BAZ',
            ('SPAM', 42),
            ('EGGS', 9001),
        )
        
    assert issubclass(Blag, FakeEnum)
    
    assert repr(Blag.FOO) == 'Blag(\'FOO\', 100)'
    assert repr(Blag.BAR) == 'Blag(\'BAR\', 101)'
    assert repr(Blag.BIZ) == 'Blag(\'BIZ\', 102)'
    assert repr(Blag.BAZ) == 'Blag(\'BAZ\', 103)'
    assert repr(Blag.SPAM) == 'Blag(\'SPAM\', 42)'
    assert repr(Blag.EGGS) == 'Blag(\'EGGS\', 9001)'
    
    assert isinstance(Blag.FOO, Blag)
    assert isinstance(Blag.BAR, Blag)
    assert isinstance(Blag.BIZ, Blag)
    assert isinstance(Blag.BAZ, Blag)
    assert isinstance(Blag.SPAM, Blag)
    assert isinstance(Blag.EGGS, Blag)
    
    assert Blag.FOO == Blag('FOO', 100)
    assert Blag.BAR == Blag('BAR', 101)
    assert Blag.BIZ == Blag('BIZ', 102)
    assert Blag.BAZ == Blag('BAZ', 103)
    assert Blag.SPAM == Blag('SPAM', 42)
    assert Blag.EGGS == Blag('EGGS', 9001)
    
    assert Blag.FOO != Blag('BAM', -1)
    assert Blag.BAR != Blag('BAM', -1)
    assert Blag.BIZ != Blag('BAM', -1)
    assert Blag.BAZ != Blag('BAM', -1)
    assert Blag.SPAM != Blag('BAM', -1)
    assert Blag.EGGS != Blag('BAM', -1)
    
    for value in Blag:
        assert (
            repr(value) == 'Blag(\'{}\', {})'.format(value.name, value.value)
        )
        
    print "All tests passed!"
    
    return 0
    
    
if __name__ == '__main__':
    sys.exit(_test())
    