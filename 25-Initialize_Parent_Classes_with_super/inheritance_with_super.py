from pprint import pprint


class MyBaseClass:
    def __init__(self, value):
        self.value = value


class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 5


class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 2


class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super().__init__(value)


foo = GoodWay(5)
print('Should be 5 * (5 + 2) = 35 and is', foo.value)


print('See the mro() method:\n')
pprint(GoodWay.mro())
print('\nMyBaseClass is called once')
