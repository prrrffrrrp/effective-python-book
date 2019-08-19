import logging


#  Private attr. can be reached inside of the class:
class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


foo = MyObject()
assert foo.public_field == 5

assert foo.get_private_field() == 10

#  But, not possible to access private attr. from the outside of the class:
try:
    foo.__private_field
except:
    logging.exception('Expected\n')
else:
    assert False
#  print(foo._MyObject__private_field)


#  Private attributes can be accessed through classmethods because they are
#  declared inside the class
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field


bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71


#  Subclasses cannot access private attr from the parent class
try:
    class MyParentObject:
        def __init__(self):
            self.__private_field = 71

    class MyChildObject(MyParentObject):
        def get_private_field(self):
            return self.__private_field

    baz = MyChildObject()
    baz.get_private_field()
except:
    logging.exception('Expected\n')
else:
    assert False

# When printing the instance dict we see that the private attr has, internally,
# another name.
print(baz.__dict__)
assert baz._MyParentObject__private_field == 71


# MyIntergerSubClass cannot access the private attr like that:
class MyBaseClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value


class MyClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())


spam = MyClass(5)
assert spam.get_value() == '5'


class MyIntergerSubclass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)
    # Should be self._MyBaseClass__value


try:
    foo = MyIntergerSubclass(5)
    foo.get_value()
except:
    logging.exception('Expected\n')
else:
    assert False


# It is possible to use protected attrs (they should be documented):
class MyClass:
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned for
        # the object it should be treated as immutable.
        self._value = value

    def get_value(self):
        return str(self._value)


class MyIntergerSubclass(MyClass):
    def get_value(self):
        return self._value


foo = MyIntergerSubclass(5)
assert foo.get_value() == 5


# but, attention:
class ApiClass:
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts


a = Child()
print(a.get(), 'and', a._value, 'should be different')


# Private attr can be used when the Parent and the child have attrs with
# the same name that should/could contain different values:
class ApiClass:
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # OK!


a = Child()
print(a.get(), 'and', a._value, 'are different')
