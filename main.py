from expression import Expression
from _expression_topostfix import infix_to_postfix
from _expression_evaluation import evaluate_expression


def testing_polish(string):
    exp = Expression(string)
    tokens = exp.get_tokens()
    postfix = infix_to_postfix(tokens)
    value,evaluated,error = evaluate_expression(postfix,0x2000,{'PEPE':20,'holis':10})
    print('\n'+string)
    print(f'{tokens}')
    print(f'{postfix}')
    print(f'{value}\nEvaluated = {evaluated}\nError = {error}')

# testing_polish('A*B+C*D&E*F+G*H')
# testing_polish('3+4')
# testing_polish('3+4-2+7')
# testing_polish('2+3*4')
# testing_polish('2*3+4')
# testing_polish('3+.NOT..HIGH.2*5')

# testing_polish('2*(3+4)/(1-5)')
# testing_polish('#2')

testing_polish('(1.SHL.31)-1')
testing_polish('PEPE+*')
testing_polish('HOLIS+holis')
testing_polish('\'ABCD\'')
testing_polish('\'\'\'')
testing_polish('\'\'')
testing_polish('\'')
