from compileroperator import is_binary_operator,is_unary_operator,is_variable,get_binary_operator,get_unary_operator
from compileroperator import CompilerOperator

def infix_to_postfix(tokens : list[str]) -> list[list[str, CompilerOperator],bool]: # bool = error
    postfix = []
    stack = []
    expects_variable = True
    error = False

    for token in tokens:
        if expects_variable:
            if is_variable(token):
                postfix.append(token)
                expects_variable = False
            elif token == '(':
                stack.append(token)
            elif is_unary_operator(token):
                stack.append(get_unary_operator(token))
            else:
                print(f'ERROR: invalid variable: {token}')
                error = True
                break
        else: # not expects_variable:
            if is_binary_operator(token):
                new_operator = get_binary_operator(token)
                while len(stack) != 0 \
                    and type(stack[-1]) == CompilerOperator \
                        and stack[-1].order <= new_operator.order: # not '(', also, binary operators are always left associative
                    postfix.append(stack.pop())
                stack.append(new_operator)
                expects_variable = True
            elif token == ')':
                while len(stack) != 0 and type(stack[-1]) == CompilerOperator:
                    postfix.append(stack.pop())
                if len(stack) == 0 or stack[-1] != '(':
                    print(f'ERROR: mismatched parentheses')
                    error = True
                    break
                else:
                    stack.pop()
            else:
                print(f'ERROR: invalid operator: {token}')
                error = True
                break

    while not error and len(stack) != 0:
        if stack[-1] == '(':
            print(f'ERROR: mismatched parentheses')
            error = True
            break     
        elif type(stack[-1]) == CompilerOperator:
            postfix.append(stack.pop())
        else:
            print(f'ERROR: unknown TOS: {stack[-1]}')
            error = True
            break

    return [postfix if not error else [],error]

