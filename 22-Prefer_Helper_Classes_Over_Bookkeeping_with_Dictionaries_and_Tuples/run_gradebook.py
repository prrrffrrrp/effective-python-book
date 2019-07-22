from gradebook import Grade, Subject, Student, Gradebook


book = Gradebook()
albert = book.student('Albert Einstein')

math_albert = albert.subject('Maths')
math_albert.report_grade(80, 0.10)

physics_albert = albert.subject('Physics')
physics_albert.report_grade(90, 0.20)


print(albert.average_grade())
print(albert.subject('Maths'))
