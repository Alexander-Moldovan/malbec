from numpy import int32

NO_OPERAND_EXPECTED = 0
OPERAND_IS_SINGLE_VARIABLE = 1
OPERAND_IS_ARRAY_OF_REGULAR = 2
OPERAND_IS_SINGLE_STRING = 3

class Directive(object):
    def __init__(self, name:str,requires_operand:bool,
                 label_required = False,
                 generates_code = False,
                 reset_offset = False,
                 operand_type = NO_OPERAND_EXPECTED,
                 operand_min = 0, operand_max = 0, operand_size_in_bytes = 0) -> None:
        self.name = name
        self.requires_operand = requires_operand

        self.label_required = label_required
        self.generates_code = generates_code
        self.reset_offset = reset_offset
        self.operand_type = operand_type
        self.operand_min = operand_min
        self.operand_max = operand_max
        self.operand_size_in_bytes = operand_size_in_bytes

    def expects_no_operands(self) -> bool:
        return not self.requires_operand
    
    def expects_operands(self) -> bool:
        return self.requires_operand

DIRECTIVE_SET = {    #   name     req_oper  lab_req gen_code rstoff operand_type                op_min          op_max      op_size
    'P68H11': Directive('p68h11', False,    False,  False,   False, NO_OPERAND_EXPECTED),
    'END' :   Directive('END',    False,    False,  False,   False, NO_OPERAND_EXPECTED),
    'EQU' :   Directive('EQU',    True,     True,   False,   False, OPERAND_IS_SINGLE_VARIABLE),
    'ORG' :   Directive('ORG',    True,     False,  False,   True,  OPERAND_IS_SINGLE_VARIABLE),
    'RMB' :   Directive('RMB',    True,     False,  False,   True,  OPERAND_IS_SINGLE_VARIABLE),
    'FCB' :   Directive('FCB',    True,     False,  True,    False, OPERAND_IS_ARRAY_OF_REGULAR, int32(-128),  int32(255),  1),
    'FDB' :   Directive('FDB',    True,     False,  True,    False, OPERAND_IS_ARRAY_OF_REGULAR, int32(-32768),int32(65535),2),
    'FCC' :   Directive('FCC',    True,     False,  True,    False, OPERAND_IS_SINGLE_STRING)
}
