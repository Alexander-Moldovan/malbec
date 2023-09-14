from compileroperator import CompilerOperator
from numpy import int32

def evaluate_expression(tokens : list[str,CompilerOperator], plc: int, variable_list : dict[str,int32]) \
    -> list[int32,bool,bool]:

    evaluated = True
    error = False

    stack = []
    for token in tokens:
        if type(token) == CompilerOperator:
            if token.is_unary:
                if len(stack) >= 1:
                    a = stack.pop()
                    c,is_int = token.fn(a)
                    if is_int:
                        stack.append(c)
                    else:
                        print(f'ERROR: unary operator {token} with operand {a} resulted in a non integer {c}')
                        error = True
                        evaluated = False
                        break
                else:
                    print(f'ERROR: operator {token} needs 1 operand; stack size is {len(stack)}')
                    error = True
                    evaluated = False
                    break
            else: # is binary
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    c,is_int = token.fn(a,b)
                    if is_int:
                        stack.append(c)
                    else:
                        print(f'ERROR: binary operator {token} with operands {a} and {b} resulted in a non integer {c}')
                        error = True
                        evaluated = False
                        break                        
                else:
                    print(f'ERROR: operator {token} needs 2 operands; stack size is {len(stack)}')
                    error = True
                    evaluated = False
                    break
        elif type(token) == str: # token is variable (number, not operator), type(token) = str
            variable = 0
            if len(token) == 0:
                print(f'ERROR: invalid empty token')
                error = True
                evaluated = False
                break
            elif len(token) >= 2 and token[0] == '\'' and token[-1] == '\'':
                string = token[1:-1]
                string = string.replace('\'\'','\'')
                for c in string:
                    variable = ((variable<<8) + (ord(c) & 0xff)) & 0xffffffff
            elif token[0].isnumeric():
                if   token[-1:].upper() == 'H':
                    try:
                        variable = int(token[:-1],16)
                    except:
                        print(f'ERROR: invalid token: {token}')
                        error = True
                        evaluated = False
                        break                        
                elif token[-1:].upper() == 'B':
                    try:
                        variable = int(token[:-1],2)
                    except:
                        print(f'ERROR: invalid token: {token}')
                        error = True
                        evaluated = False
                        break  
                elif token[-1:].upper() == 'Q':
                    try:
                        variable = int(token[:-1],8)
                    except:
                        print(f'ERROR: invalid token: {token}')
                        error = True
                        evaluated = False
                        break  
                else:
                    try:
                        variable = int(token,10)
                    except:
                        print(f'ERROR: invalid token: {token}')
                        error = True
                        evaluated = False
                        break  
            elif token[0] == '$':
                try:
                    variable = int(token[1:],16)
                except:
                    print(f'ERROR: invalid token: {token}')
                    error = True
                    evaluated = False
                    break
            elif token == '*':
                if plc != None:
                    variable = plc
                else:
                    evaluated = False # El PLC no esta definido!!!
                    break                    
            elif token[0].isalpha() or token[0] in ['?','@','_']:
                if token in variable_list:
                    variable = variable_list[token]
                else:
                    evaluated = False # No encontró una variable en la lista!!!
                    break
            else:
                print(f'ERROR: invalid token: {token}')
                error = True
                evaluated = False
                break                
        
            variable = int32(int32(-1) & variable)
            stack.append(variable)
        else:
            print(f'ERROR: unknown token: {token} of type {type(token)}')
            error = True
            evaluated = False
            break

    if evaluated and len(stack) != 1:
        print(f'ERROR: stack size is {len(stack)} instead of 1')
        error = True
        evaluated = False

    return stack[-1] if evaluated else int32(0), evaluated, error

