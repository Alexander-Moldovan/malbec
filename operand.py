from expression import Expression
from addressingmodes import *
from numpy import int32,uint32

REL_OFFSET_LIST = {EXT: 2, DIR_MSK_REL: 4, INDX_MSK_REL: 4, INDY_MSK_REL: 5} # (doesnt distinguish among EXT, DIR or REL)

class Operand(object): # Made of expressions, separated by commas
    def __init__(self, operand = "", relative = False) -> None:
        self._set_operand(operand, relative)

    def __repr__(self):
        s = ''
        for e in self.expressions:
            s += f'{e},'
        s = s[:-1]
        return f'{self.original_string :<20} -> {s}'
    
    def _set_operand(self, operand : str, relative : bool):
        self.original_string = operand
        self.expressions = [Expression(expr_str) for expr_str in operand.split(',')]
        self.own_addmode = self._get_addressing_mode()
        if relative:
            if self.own_addmode in REL_OFFSET_LIST: 
                offset = REL_OFFSET_LIST[self.own_addmode]
                new_expr_str = f'({operand.split(",")[-1]})-(*+{offset})' # TODO: checkear que exista posicion [-1]
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
    
    # def get_32bit_operand(self) -> list[int32,bool,bool]:
    #     error = False
    #     operands = 0

    #     evaluated = not self.needs_evaluation()
    #     if self.own_addmode == EXT:
    #         operands = self.expressions[0].get_value()
    #     else:
    #         error = True
    #     return operands,evaluated,error

    # TODO: resolver tema de REL, porq no evalua expresion tal, sino la resta!!!
    # (incluye los DIR_MSK_REL, INDX_MSK_REL y INDY_MSK_REL)
    def get_operands(self, addressing_mode) -> list[str,bool,bool]: # TODO: tirar warnings si se va de rango (y lo mismo para las directivas)
        error = False   
        operands = ''

        # aca asumo q me pidieron bien los add_modes

        evaluated = not self.needs_evaluation()

        if self.own_addmode == INH:
            operands = f''

        elif self.own_addmode == IMM16:
            imm16 = uint32(self.expressions[0].get_value())
            if addressing_mode == IMM16:
                operands = f'{imm16 :04X}'[-4:]
            elif addressing_mode == IMM:
                operands = f'{imm16 :02X}'[-2:]
            else:
                print(f'ERROR: specified addressing mode {addressing_mode} not compatible with {self.own_addmode}')
                operands = ''
                error = True

        elif self.own_addmode == EXT: # TODO: hacer funcion dir
            extadd = uint32(self.expressions[0].get_value())
            if addressing_mode == EXT:
                operands = f'{extadd :04X}'[-4:]
            elif addressing_mode == DIR or addressing_mode == REL:
                operands = f'{extadd :02X}'[-2:]
            else:
                print(f'ERROR: specified addressing mode {addressing_mode} not compatible with {self.own_addmode}')
                operands = ''
                error = True

        elif self.own_addmode == INDX or self.own_addmode == INDY:
            indoff = uint32(self.expressions[0].get_value())
            operands = f'{indoff :02X}'[-2:]

        elif self.own_addmode == DIR_MSK:
            diradd = uint32(self.expressions[0].get_value())
            mask = uint32(self.expressions[1].get_value())
            operands = f'{diradd :02X}'[-2:] + f'{mask :02X}'[-2:] # TODO: check order

        elif self.own_addmode == INDX_MSK or self.own_addmode == INDY_MSK:
            indoff = uint32(self.expressions[0].get_value())
            mask = uint32(self.expressions[2].get_value())
            operands = f'{indoff :02X}'[-2:] + f'{mask :02X}'[-2:] # TODO: check order

        elif self.own_addmode == DIR_MSK_REL:
            diradd = uint32(self.expressions[0].get_value())
            mask = uint32(self.expressions[1].get_value())
            rel = uint32(self.expressions[2].get_value())
            operands = f'{diradd :02X}'[-2:] + f'{mask :02X}'[-2:] + f'{rel :02X}'[-2:] # TODO: check order

        elif self.own_addmode == INDX_MSK_REL or self.own_addmode == INDY_MSK_REL:
            indoff = uint32(self.expressions[0].get_value())
            mask = uint32(self.expressions[2].get_value())
            rel = uint32(self.expressions[3].get_value())
            operands = f'{indoff :02X}'[-2:] + f'{mask :02X}'[-2:] + f'{rel :02X}'[-2:] # TODO: check order
        else:
            print(f'ERROR: invalid addressing mode {self.own_addmode}')
            operands = ''
            error = True

        return operands,evaluated,error


############## ORG / EQU / RMB ###########################
    def operand_is_single_variable(self) -> bool:
        return self.check_addressing_mode(EXT)

    def get_operand_single_variable(self, none = None) -> list[int32,bool,bool]:
        error = False
        operands = 0

        evaluated = not self.needs_evaluation()
        if self.own_addmode == EXT:
            operands = self.expressions[0].get_value()
        else:
            error = True
        return operands,evaluated,error


############## FCB / FDB ###########################

    def operand_is_array_of_regular(self) -> bool:
        if len(self.expressions) == 0:
            return False
        answer = True
        for expression in self.expressions:
            if not expression.is_regular_expression():
                answer = False
                break
        return answer
    def get_operand_array_of_regular(self, min_max_size: list[int]) -> list[str,bool,bool]:
        error = False
        operands = ''

        expression_min,expression_max,expression_size_in_bytes = min_max_size

        evaluated = not self.needs_evaluation()
        if self.operand_is_array_of_regular():
            for expression in self.expressions:
                value = expression.get_value()
                if expression_min <= value <= expression_max:
                    operands += f'{value :08X}'[-(2*expression_size_in_bytes):]
                else:
                    error = True
                    break
        else:
            error = True
        return operands,evaluated,error            

    # def check_only_regular_expressions(self):
    #     if len(self.expressions) == 0:
    #         return False
    #     answer = True
    #     for expression in self.expressions:
    #         if not expression.is_regular_expression():
    #             answer = False
    #             break
    #     return answer
    # def get_regular_expressions(self,expression_min,expression_max,expression_size_in_bytes) -> list[str,bool,bool]:
    #     error = False
    #     operands = ''

    #     evaluated = not self.needs_evaluation()
    #     if self.check_only_regular_expressions():
    #         for expression in self.expressions:
    #             value = expression.get_value()
    #             if expression_min <= value <= expression_max:
    #                 operands += f'{value :08X}'[-(2*expression_size_in_bytes):]
    #             else:
    #                 error = True
    #                 break
    #     else:
    #         error = True

    #     return operands,evaluated,error    

    def get_ammount_of_expressions(self):
        return len(self.expressions)


############## FCC ###########################
    # TODO: CORREGIR: problemas con , o ESPACIOS en strings

    def operand_is_single_string(self) -> bool:
        return len(self.expressions) == 1 and self.expressions[0].is_single_string()
    def get_operand_single_string(self, none = None) -> list[str,bool,bool]:
        evaluated = not self.needs_evaluation()
        if self.operand_is_single_string():
            operands,error = self.expressions[0].get_string()
            evaluated = True # TODO: modificarlo
        else:
            operands = ''
            error = True
        return operands,evaluated,error

    # def check_single_string(self):
    #     return len(self.expressions) == 1 and self.expressions[0].is_single_string()
    # def get_single_string(self) -> list[str,bool]:
    #     if self.check_single_string():
    #         operands,error = self.expressions[0].get_string()
    #     else:
    #         operands = ''
    #         error = True
    #     return operands,error # No 'evaluated' variable since a string is always 'evaluated'


#############################################

    
    def is_value_direct(self) -> bool:
        if self.own_addmode == EXT:
            if not self.needs_evaluation():
                return 0 <= self.expressions[0].get_value() < 256
            else:
                return False
        else:
            return False

    def check_addressing_mode(self, addressing_mode) -> bool: # Comprobar por afuera entre EXT, DIR y REL; y entre IMM16 y IMM
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
