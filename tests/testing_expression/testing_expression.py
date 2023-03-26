from expression import Expression

def testing_expression(string):
    exp = Expression(string)
    print('\n'+string)
    print(f'{exp.expression}')

testing_expression('HOLA.AND.ADIOS')
testing_expression('2+4+PEPE/PEPINO')
testing_expression('2h+PEPE02')
