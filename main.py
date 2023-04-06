from expression import Expression
from _expression_topostfix import infix_to_postfix

def testing_polish(string):
    exp = Expression(string)
    print('\n'+string)
    print(f'{exp.get_tokens()}')
    print(f'{infix_to_postfix(exp.get_tokens())}')


testing_polish('A*B+C*D&E*F+G*H')
testing_polish('3+4')
testing_polish('3+4-2+7')
testing_polish('2+3*4')
testing_polish('2*3+4')
testing_polish('3+.NOT..HIGH.2*5')

testing_polish('2*(3+4)/(1-5)')
testing_polish('#2')