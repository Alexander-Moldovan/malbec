from expression import Expression
from addressingmodes import *
from numpy import int32

REL_OFFSET_LIST = {EXT: 2, DIR_MSK_REL: 4, INDX_MSK_REL: 4, INDY_MSK_REL: 5} # (doesnt distinguish among EXT, DIR or REL)

class Operand(object): # Made of expressions, separated by commas
    def __init__(self, operand = "", relative = False) -> None:
        self._set_operand(operand, relative)

    def __repr__(self):
        return self.original_string
    
    def _set_operand(self, operand : str, relative : bool):
        self.original_string = operand
        self.expressions = [Expression(expr_str) for expr_str in operand.split(',')]
        self.own_addmode = self._get_addressing_mode()
        if relative:
            if self.own_addmode in REL_OFFSET_LIST: 
                offset = REL_OFFSET_LIST[self.own_addmode]
                new_expr_str = f'({operand.split(",")[-1]})-(*+{offset})'
                self.expressions[-1] = Expression(new_expr_str)

                # print(f'OLD ADDRESSING MODE = {self.own_addmode}')
                # self.own_addmode = self._get_addressing_mode()
                # print(f'NEW ADDRESSING MODE = {self.own_addmode}')
                # print(f'NEW EXPRESSION = {new_expr_str}')
            # else: 
            #   an error is bound to happen when evaluating the opperand

        # if self.own_addmode == REL:
        #     expr_str = '(' + expr_str + ')-(*+2)'
        #     self.expressions[0] = Expression(expr_str)
        #     print(f'New expr is {expr_str}' )

    def needs_evaluation(self):
        answer = False
        for expression in self.expressions:
            if expression.need_evaluation():
                answer = True
                break
        return answer
    
    def evaluate(self, plc:int, variable_list : dict[str,int32]) -> list[bool,bool]: #return evaluated,error
        evaluated = True
        error = False
        for expression in self.expressions:
            if expression.need_evaluation():
                expression_is_evaluated,error = expression.evaluate(plc,variable_list)
                evaluated = evaluated and expression_is_evaluated
                if error:
                    break
        return evaluated,error # evaluated only true if all evaluable expressions are evaluated
    
    # TODO: resolver tema de REL, porq no evalua expresion tal, sino la resta!!!
    # (incluye los DIR_MSK_REL, INDX_MSK_REL y INDY_MSK_REL)
    def get_operands(self, addressing_mode) -> list[str,bool,bool]:
        error = False   
        operands = ''

        # aca asumo q me pidieron bien los add_modes

        evaluated = not self.needs_evaluation()
        if self.own_addmode == INH:
            operands = f''
        elif self.own_addmode == IMM16: # NOTA: distinguir caso IMM y IMM16
            imm16 = self.expressions[0].get_value()
            operands = f'{imm16 : 04X}'[-4:]
        elif self.own_addmode == EXT: # NOTA: distinguir caso EXT, DIR y REL
            extadd = self.expressions[0].get_value()
            operands = f'{extadd : 04X}'[-4:]
        elif self.own_addmode == INDX or self.own_addmode == INDY:
            indoff = self.expressions[0].get_value()
            operands = f'{indoff : 02X}'[-2:]
        elif self.own_addmode == DIR_MSK:
            diradd = self.expressions[0].get_value()
            mask = self.expressions[1].get_value()
            operands = f'{diradd : 02X}'[-2:] + f'{mask : 02X}'[-2:] # TODO: check order
        elif self.own_addmode == INDX_MSK or self.own_addmode == INDY_MSK:
            indoff = self.expressions[0].get_value()
            mask = self.expressions[2].get_value()
            operands = f'{indoff : 02X}'[-2:] + f'{mask : 02X}'[-2:] # TODO: check order
        elif self.own_addmode == DIR_MSK_REL:
            diradd = self.expressions[0].get_value()
            mask = self.expressions[1].get_value()
            rel = self.expressions[2].get_value()
            operands = f'{diradd : 02X}'[-2:] + f'{mask : 02X}'[-2:] + f'{rel : 02X}'[-2:] # TODO: check order
        elif self.own_addmode == INDX_MSK_REL or self.own_addmode == INDY_MSK_REL:
            indoff = self.expressions[0].get_value()
            mask = self.expressions[2].get_value()
            rel = self.expressions[3].get_value()
            operands = f'{indoff : 02X}'[-2:] + f'{mask : 02X}'[-2:] + f'{rel : 02X}'[-2:] # TODO: check order
        else:
            print(f'ERROR: invalid addressing mode {self.own_addmode}')
            operands = ''
            error = True

        return operands,evaluated,error


    def check_addressing_mode(self, addressing_mode) -> bool: # Comprobar por afuera que sea EXT, DIR o REL
        # own_addmode = self._get_addressing_mode()
        if(self.own_addmode == EXT):
            return addressing_mode == EXT or addressing_mode == DIR or addressing_mode == REL
        elif(self.own_addmode == IMM16):
            return addressing_mode == IMM or addressing_mode == IMM16
        else:
            return addressing_mode == self.own_addmode

    def _get_addressing_mode(self): # Warning: no distingue entre DIR, EXT o REL
        if len(self.expressions) == 0:
            return INH # Cambio de diseño: ahora [] equivale a INH
        elif len(self.expressions) == 1:
            if(self.expressions[0].is_empty()): # Warning! No debería haber expresiones vacias! este codigo es preventivo
                return INH
            elif(self.expressions[0].is_imm_expression()):
                return IMM16  # por defecto, se asume IMM16. IMM tendrá que comprobar aparte
            elif(self.expressions[0].is_regular_expression()):
                return EXT  # por defecto, se asume EXT. DIR o REG tendrán que comprobar aparte
            else:
                return UNDEFINED_ADDRESSING_MODE # TODO: darle uso
        elif len(self.expressions) == 2:
            if(self.expressions[0].is_regular_expression() and self.expressions[1].is_index()):
                if self.expressions[1].is_index_x():
                    return INDX
                elif self.expressions[1].is_index_y():
                    return INDY
                else:
                    return UNDEFINED_ADDRESSING_MODE
            elif(self.expressions[0].is_regular_expression() and self.expressions[1].is_imm_expression()):
                return DIR_MSK
            else:
                return UNDEFINED_ADDRESSING_MODE
        elif len(self.expressions) == 3:
            if(self.expressions[0].is_regular_expression() and self.expressions[1].is_index() and self.expressions[2].is_imm_expression()):
                if self.expressions[1].is_index_x():
                    return INDX_MSK
                elif self.expressions[1].is_index_y():
                    return INDY_MSK
                else:
                    return UNDEFINED_ADDRESSING_MODE
            elif(self.expressions[0].is_regular_expression() and self.expressions[1].is_imm_expression() and self.expressions[2].is_regular_expression()):
                return DIR_MSK_REL
            else:
                return UNDEFINED_ADDRESSING_MODE
        elif len(self.expressions) == 4:
            if(self.expressions[0].is_regular_expression() and self.expressions[1].is_index() and self.expressions[2].is_imm_expression() and self.expressions[3].is_regular_expression()):
                if self.expressions[1].is_index_x():
                    return INDX_MSK_REL
                elif self.expressions[1].is_index_y():
                    return INDY_MSK_REL
                else:
                    return UNDEFINED_ADDRESSING_MODE
            else:
                return UNDEFINED_ADDRESSING_MODE
        else:
            return UNDEFINED_ADDRESSING_MODE
