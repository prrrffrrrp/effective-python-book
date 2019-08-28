import logging


# Non pythonic way
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


print('\n--OldResistor--\n')
r0 = OldResistor(50e3)
print(f'Before: {r0.get_ohms()}')
r0.set_ohms(10e3)
print(f'After: {r0.get_ohms()}')

print(r0.set_ohms(r0.get_ohms() + 5e3))
print(f'AfterAfter: {r0.get_ohms()}')


# The simplest way
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


print('\n--Resistor--\n')
r1 = Resistor(50e3)
r1.ohms = 10e3
print(f'{r1.ohms} ohms, {r1.voltage} voltage, {r1.current} current')

r1.ohms += 5e3


# Use property to modify behavior
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self.voltage / self.ohms


print('\n--VoltageResistance--\n')
r2 = VoltageResistance(1e3)
print(f'Before: {r2.current} amps')
r2.voltage = 10
print(f'After: {r2.current} amps')


# property can be used to check some condition. That condition is evaluated
# during instantiation. If it is not fullfilled, the instance is not
# constructed.
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'{ohms} ohms must be > 0')
        self._ohms = ohms


try:
    r3 = BoundedResistance(1e3)
    r3.ohms = 0
except:
    logging.exception('\nBoundedResistance - Expected')
else:
    assert False

try:
    BoundedResistance(-5)
except:
    logging.exception('\nBoundedResistance - Expected')
else:
    assert False


# Here @property is used to make sure that a Parent's class attribute
# is not modifiable from the child instance.
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms


try:
    r4 = FixedResistance(1e3)
    r4.ohms = 2e3
except:
    logging.exception('\nFixedResistance - Expected')
else:
    assert False


# Do not implement special behavior in the getter. Use the setter method for
# that. Otherwhise there might be strange results.
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms


print('\n--MysteriousResistor--\n')
r7 = MysteriousResistor(10)
r7.current = 0.01
print(f"Before: {r7.voltage}")
r7.ohms
print(f"After: {r7.voltage}")
