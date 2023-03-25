class Directive(object):
    def __init__(self, name:str,requires_operand:bool) -> None:
        self.name = name
        self.requires_operand = requires_operand

    def expects_no_operands(self) -> bool:
        return not self.requires_operand
    
    def expects_operands(self) -> bool:
        return self.requires_operand

DIRECTIVE_SET = {
    'P68H11': Directive('p68h11', False),
    'END' : Directive('END', False),
    'EQU' : Directive('EQU', True),
    'ORG' : Directive('ORG', True),
    'RMB' : Directive('RMB', True),
    'FCB' : Directive('FCB', True),
    'FDB' : Directive('FDB', True),
    'FCC' : Directive('FCC', True)
}
