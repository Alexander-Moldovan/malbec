from expression import Expression
from polishnotation import expression_to_polish

def testing_polish(string):
    exp = Expression(string)
    print('\n'+string)
    print(f'{exp.expression}')


    print(f'{expression_to_polish(exp)}')


testing_polish('A*B+C*D&E*F+G*H')
