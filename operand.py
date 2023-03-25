from expression import Expression
from addressingmodes import *

class Operand(object): # Made of expressions, separated by commas
    def __init__(self, operand = "") -> None:
        self.set_operand(operand)

    def set_operand(self, operand : str):
        self.operand = [Expression(expr_str) for expr_str in operand.split(',')]

    def check_addressing_mode(self, addressing_mode) -> bool: # Comprobar por afuera que sea EXT, DIR o REL
        own_addmode = self._get_addressing_mode()
        if(own_addmode == EXT):
            return addressing_mode == EXT or addressing_mode == DIR or addressing_mode == REL
        else:
            return addressing_mode == own_addmode

    def _get_addressing_mode(self): # Warning: no distingue entre DIR, EXT o REL
        if len(self.operand) == 0:
            return INH # Warning! No debería usarse Operand sin operandos. Este caso es preventivo
        elif len(self.operand) == 1:
            if(self.operand[0].is_empty()): # Warning! No debería usarse Operand sin operandos. Este caso es preventivo
                return INH
            elif(self.operand[0].is_imm_expression()):
                return IMM
            elif(self.operand[0].is_regular_expression()):
                return EXT  # por defecto, se asume EXT. DIR o REG tendrán que comprobar aparte
            else:
                return INVALID_ADDRESSING_MODE # TODO: darle uso
        elif len(self.operand) == 2:
            if(self.operand[0].is_regular_expression() and self.operand[1].is_index()):
                if self.operand[1].is_index_x():
                    return INDX
                elif self.operand[1].is_index_y():
                    return INDY
                else:
                    return INVALID_ADDRESSING_MODE
            elif(self.operand[0].is_regular_expression() and self.operand[1].is_imm_expression()):
                return DIR_MSK
            else:
                return INVALID_ADDRESSING_MODE
        elif len(self.operand) == 3:
            if(self.operand[0].is_regular_expression() and self.operand[1].is_index() and self.operand[2].is_imm_expression()):
                if self.operand[1].is_index_x():
                    return INDX_MSK
                elif self.operand[1].is_index_y():
                    return INDY_MSK
                else:
                    return INVALID_ADDRESSING_MODE
            elif(self.operand[0].is_regular_expression() and self.operand[1].is_imm_expression() and self.operand[2].is_regular_expression()):
                return DIR_MSK_REL
            else:
                return INVALID_ADDRESSING_MODE
        elif len(self.operand) == 4:
            if(self.operand[0].is_regular_expression() and self.operand[1].is_index() and self.operand[2].is_imm_expression() and self.operand[3].is_regular_expression()):
                if self.operand[1].is_index_x():
                    return INDX_MSK_REL
                elif self.operand[1].is_index_y():
                    return INDY_MSK_REL
                else:
                    return INVALID_ADDRESSING_MODE
            else:
                return INVALID_ADDRESSING_MODE
        else:
            return INVALID_ADDRESSING_MODE
        
    

    #     for originalstring in operand.split(','):
    #         self.data.append(self._split_operations_and_variables(originalstring))

    # def _split_operations_and_variables(self,originalstring:str) -> str:
    #     return []

# op = Operand("$200,x")
# print(len(op.operand))
# print(op.operand[0].is_index())

# print(op.operand[1].is_index())