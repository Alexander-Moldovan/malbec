from expression import Expression
from compileroperator import CompilerOperator,is_binary_operator,is_unary_operator,is_variable,get_unary_operator,get_binary_operator

# TODO hacer

# TODO: cambiar "partícula" por "token" (Lexical analysis)

# implementing Shunting yard algorithm

def expression_to_postfix(expression: Expression) -> list:
    postfix = []
    stack = []
    error = False

    for token in expression.get_particles():
        

        pass

    if error:
        return []
    else:
        return postfix

# def expression_to_polish(expression: Expression) -> list:
#     polish = []
#     expects_operator = False
#     error = False
#     for particle in expression.get_particles():
#         if not expects_operator:
#             if is_variable(particle):
#                 polish.append(particle)
#                 expects_operator = True
#             elif is_unary_operator(particle):
#                 polish.append(get_unary_operator(particle))
#             else:
#                 error = True
#                 break
#         else:
#             if is_binary_operator(particle):
#                 operator = get_binary_operator(particle)
#                 order = operator.order()
#                 last_valid_place = len(polish)-1
#                 for index in reversed(range(0,len(polish))):
#                     if type(polish[index]) == CompilerOperator:
#                         if order < polish[index].order():
#                             break
#                         else:
#                             last_valid_place = index
#                 polish.insert(last_valid_place,operator)
#                 expects_operator = False
#             else:
#                 error = True
#                 break
#     if error:
#         return []
#     else:
#         return polish
