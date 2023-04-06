_NEW_TOKEN = 0
_DOT_OPERAND  = 1
_LESS_THAN    = 2
_MORE_THAN    = 3
_ALPHANUMERIC = 4
_REG_NUMBER   = 5
_HEX_NUMBER   = 6
_APOSTROPHE_1 = 7
_APOSTROPHE_2 = 8

#TODO: releer para ver si con tokens tiene sentido

class Expression(object): # Made of tokens (operators, variables, etc)
    def __init__(self, expression = "") -> None:
        self.set_expression(expression)

    def set_expression(self, expression : str):
        self.expression = []

        state = _NEW_TOKEN
        current_token = ''
        for c in expression: # c is a 'char'
            processed_character = False
            if state != _NEW_TOKEN:
                if state == _DOT_OPERAND:
                    current_token += c
                    processed_character = True
                    if c == '.':
                        self.expression.append(current_token)
                        current_token = ''
                        state = _NEW_TOKEN
                elif state == _LESS_THAN:
                    if c in ['<','=','>']:
                        current_token += c
                        processed_character = True
                        self.expression.append(current_token)
                        current_token = ''
                        state = _NEW_TOKEN
                    else:
                        self.expression.append(current_token)
                        current_token = ''
                elif state == _MORE_THAN:
                    if c in ['=','>']:
                        current_token += c
                        processed_character = True
                        self.expression.append(current_token)
                        current_token = ''
                        state = _NEW_TOKEN
                    else:
                        self.expression.append(current_token)
                        current_token = ''
                elif state == _ALPHANUMERIC:
                    if c.isalpha() or c.isnumeric() or c in ['?','@','_','$']:
                        current_token += c
                        processed_character = True
                    else:
                        self.expression.append(current_token)
                        current_token = ''
                        state = _NEW_TOKEN
                elif state == _REG_NUMBER:
                    if c.isnumeric():
                        current_token += c
                        processed_character = True
                    elif c.upper() in ['H','B','Q']:
                        current_token += c.upper()
                        processed_character = True
                        self.expression.append(current_token)
                        current_token = ''
                        state = _NEW_TOKEN
                    else:
                        self.expression.append(current_token)
                        current_token = ''
                elif state == _HEX_NUMBER:
                    if c.isnumeric():
                        current_token += c
                        processed_character = True
                    else:
                        self.expression.append(current_token)
                        current_token = ''
                elif state == _APOSTROPHE_1:
                    current_token += c
                    processed_character = True
                    if c == '\'':
                        state = _APOSTROPHE_2
                elif state == _APOSTROPHE_2:
                    if c == '\'':
                        current_token += c
                        processed_character = True
                        state = _APOSTROPHE_1
                    else:
                        self.expression.append(current_token)
                        current_token = ''

            if not processed_character: # Therefore, new token (operator or variable)
                if current_token != "":
                    print(f'ERROR: {current_token} discarted')
                    current_token = ""

                if c in ['&','+','-','*','/','=','(',')','#']:
                    self.expression.append(c)
                    state = _NEW_TOKEN
                elif c == '.':
                    current_token = c
                    state = _DOT_OPERAND
                elif c == '<':
                    current_token = c
                    state = _LESS_THAN
                elif c == '>':
                    current_token = c
                    state = _MORE_THAN
                elif c.isalpha() or c in ['?','@','_']:
                    current_token = c
                    state = _ALPHANUMERIC
                elif c.isnumeric():
                    current_token = c
                    state = _REG_NUMBER
                elif c == '$':
                    current_token = c
                    state = _HEX_NUMBER
                elif c == '\'':
                    current_token = c
                    state = _APOSTROPHE_1
        if current_token != '': # TODO: corroborar que sea válido
            self.expression.append(current_token)

    def get_tokens(self) -> list[str]: #TODO: determinar si es necesario este metodo
        return self.expression

    def is_index(self) -> bool:
        return len(self.expression) == 1 and self._is_token_index(self.expression[0])
    
    def is_index_x(self) -> bool:
        return len(self.expression) == 1 and self._is_token_x(self.expression[0])
    
    def is_index_y(self) -> bool:
        return len(self.expression) == 1 and self._is_token_y(self.expression[0])
    
    def is_imm_expression(self) -> bool:
        return len(self.expression) > 0 and self._is_token_numsign(self.expression[0])

    def is_regular_expression(self) -> bool:
        return not self.is_index() and not self.is_imm_expression() and not self.is_empty()

    def is_empty(self) -> bool:
        return len(self.expression) == 0    

    def _is_token_index(self,token:str) -> bool:
        return self._is_token_x(token) or self._is_token_y(token)

    def _is_token_x(self,token:str) -> bool:
        return token.upper() == 'X'
    
    def _is_token_y(self,token:str) -> bool:
        return token.upper() == 'Y'
    
    def _is_token_numsign(self,token:str) -> bool:
        return token == '#'
