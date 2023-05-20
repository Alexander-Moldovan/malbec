from operand import Operand
from addressingmodes import *
from numpy import int16, uint16

class ProcessedLine(object):
    def __init__(self, source_line_number : int,source_line : str, address = None, code = "", addressing_mode = UNDEFINED_ADDRESSING_MODE, label = None, instruction = None, operand = '', relative_operand = False) -> None:
        self.source_line_number = source_line_number
        self.source_line = source_line

        self.address = address
        self.code = code
        self.addmode = addressing_mode
        self.set_label(label)
        self.set_instruction(instruction)
        self.set_operand(operand,relative_operand)

    def has_content(self):
        return (self.label != None or self.instruction != None or self.operand != None)

    def set_label(self,label:str):
        self.label = label
    def set_instruction(self,instruction:str):
        self.instruction = instruction
    def set_operand(self,operand:str, relative : bool):
        self.operand = Operand(operand,relative)

    def __repr__(self): #TODO: cambiar el modo de acceder al addmode
        address = f'{uint16(self.address):04X}' if self.address != None else "----"
        return f'ADD:{address}\tCODE:{self.code : <8}\tADDMODE:{"---" if self.addmode == UNDEFINED_ADDRESSING_MODE else self.addmode}\tLABEL:{self.label if self.label!=None else " " :<16}\tINST:{self.instruction}\tOPER:{self.operand}'
