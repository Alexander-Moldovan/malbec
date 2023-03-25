_NEW_PARTICLE = 0
_DOT_OPERAND  = 1
_LESS_THAN    = 2
_MORE_THAN    = 3
_ALPHANUMERIC = 4
_REG_NUMBER   = 5
_HEX_NUMBER   = 6
_APOSTROPHE_1 = 7
_APOSTROPHE_2 = 8

class Expression(object): # Made of particles (operators, variables, etc)
    def __init__(self, expression = "") -> None:
        self.set_expression(expression)

    def set_expression(self, expression : str):
        self.expression = []

        state = _NEW_PARTICLE
        current_particle = ''
        for c in expression:
            processed_character = False
            if state != _NEW_PARTICLE:
                if state == _DOT_OPERAND:
                    current_particle += c
                    processed_character = True
                    if c == '.':
                        self.expression.append(current_particle)
                        current_particle = ''
                        state = _NEW_PARTICLE
                elif state == _LESS_THAN:
                    if c in ['<','=','>']:
                        current_particle += c
                        processed_character = True
                        self.expression.append(current_particle)
                        current_particle = ''
                        state = _NEW_PARTICLE
                    else:
                        self.expression.append(current_particle)
                        current_particle = ''
                elif state == _MORE_THAN:
                    if c in ['=','>']:
                        current_particle += c
                        processed_character = True
                        self.expression.append(current_particle)
                        current_particle = ''
                        state = _NEW_PARTICLE
                    else:
                        self.expression.append(current_particle)
                        current_particle = ''
                elif state == _ALPHANUMERIC:
                    if c.isalpha() or c.isnumeric() or c in ['?','@','_','$']:
                        current_particle += c
                        processed_character = True
                    else:
                        self.expression.append(current_particle)
                        current_particle = ''
                        state = _NEW_PARTICLE
                elif state == _REG_NUMBER:
                    if c.isnumeric():
                        current_particle += c
                        processed_character = True
                    elif c.upper() in ['H','B','Q']:
                        current_particle += c.upper()
                        processed_character = True
                        self.expression.append(current_particle)
                        current_particle = ''
                        state = _NEW_PARTICLE
                    else:
                        self.expression.append(current_particle)
                        current_particle = ''
                elif state == _HEX_NUMBER:
                    if c.isnumeric():
                        current_particle += c
                        processed_character = True
                    else:
                        self.expression.append(current_particle)
                        current_particle = ''
                elif state == _APOSTROPHE_1:
                    current_particle += c
                    processed_character = True
                    if c == '\'':
                        state = _APOSTROPHE_2
                elif state == _APOSTROPHE_2:
                    if c == '\'':
                        current_particle += c
                        processed_character = True
                        state = _APOSTROPHE_1
                    else:
                        self.expression.append(current_particle)
                        current_particle = ''

            if not processed_character: # Therefore, new operator or variable
                if current_particle != "":
                    print(f'ERROR: {current_particle} discarted')
                    current_particle = ""

                if c in ['&','+','-','*','/','=','(',')','#']:
                    self.expression.append(c)
                    state = _NEW_PARTICLE
                elif c == '.':
                    current_particle = c
                    state = _DOT_OPERAND
                elif c == '<':
                    current_particle = c
                    state = _LESS_THAN
                elif c == '>':
                    current_particle = c
                    state = _MORE_THAN
                elif c.isalpha() or c in ['?','@','_']:
                    current_particle = c
                    state = _ALPHANUMERIC
                elif c.isnumeric():
                    current_particle = c
                    state = _REG_NUMBER
                elif c == '$':
                    current_particle = c
                    state = _HEX_NUMBER
                elif c == '\'':
                    current_particle = c
                    state = _APOSTROPHE_1
                



    def is_index(self) -> bool:
        return len(self.expression) == 1 and self._is_particle_index(self.expression[0])
    
    def is_index_x(self) -> bool:
        return len(self.expression) == 1 and self._is_particle_x(self.expression[0])
    
    def is_index_y(self) -> bool:
        return len(self.expression) == 1 and self._is_particle_y(self.expression[0])
    
    def is_imm_expression(self) -> bool:
        return len(self.expression) > 0 and self._is_particle_numsign(self.expression[0])

    def is_regular_expression(self) -> bool:
        return not self.is_index() and not self.is_imm_expression() and not self.is_empty()

    def is_empty(self) -> bool:
        return len(self.expression) == 0    

    def _is_particle_index(self,particle:str) -> bool:
        return self._is_particle_x(particle) or self._is_particle_y(particle)

    def _is_particle_x(self,particle:str) -> bool:
        return particle.upper() == 'X'
    
    def _is_particle_y(self,particle:str) -> bool:
        return particle.upper() == 'Y'
    
    def _is_particle_numsign(self,particle:str) -> bool:
        return particle == '#'
