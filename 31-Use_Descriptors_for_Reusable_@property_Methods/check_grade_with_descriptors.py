# How it works:
class Grade:
    def __get__(*args, **kwargs):
        pass

    def __set__(*args, **kwargs):
        pass


class Exam:
    # class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


print('\n- First example:')
exam = Exam()

exam.writing_grade = 40
# This is the same as:
Exam.__dict__['writing_grade'].__set__(exam, 40)

print(exam.writing_grade)
# This is the same as:
print(Exam.__dict__['writing_grade'].__get__(exam, Exam))


# This is not quite right yet.
class Grade:
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value


class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


print('\n- Second example:')
first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)

second_exam = Exam()
second_exam.writing_grade = 75
print('Second', second_exam.writing_grade, 'is right')
print('First', first_exam.writing_grade, 'is wrong')
# The problem is that the writing_grade attribute is shared between instances
# of Exam. Writing_grade is able to store only one instance of a value.


# That problem can be solved by turning the value attribute into a dict and by
# tracking who sets the value and who asks for it.
class Grade:
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


print('\n- Thirth example:')
first_exam = Exam()
first_exam.writing_grade = 82

second_exam = Exam()
second_exam.writing_grade = 75
print('Second', second_exam.writing_grade, 'is right')
print('First', first_exam.writing_grade, 'is also right')


# The only problem with the code above is that refences to instances will stay
# in the _values dict even after the class instances are not used anymore or
# are deleted. That's why the WeakKeyDictionary should be used.
from weakref import WeakKeyDictionary


class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


print('\n- Thirth example:')
first_exam = Exam()
first_exam.writing_grade = 90

second_exam = Exam()
second_exam.writing_grade = 80

thirth_exam = Exam()
thirth_exam.writing_grade = 70
print('Second', second_exam.writing_grade)
print('First', first_exam.writing_grade)
print('Thirth', thirth_exam.writing_grade)

print('Deleting the thirth_exam instance...')
del thirth_exam
print('Writing_grade._values:', Exam.writing_grade._values)
for key, value in Exam.writing_grade._values.items():
    print(f'instance: {key} => grade: {value}')
