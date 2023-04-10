from operand import Operand
from addressingmodes import *
from numpy import int16

class ProcessedLine(object):
    def __init__(self, address = int16(0), code = "", addressing_mode = UNDEFINED_ADDRESSING_MODE, label = None, instruction = None, operand = '', relative_operand = False) -> None:
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
        return f'ADD:{self.address : 04X}\tCODE:{self.code}\tADDMODE:{self.operand.own_addmode}\tLABEL:{self.label if self.label!=None else " " :<8}\tINST:{self.instruction}\tOPER:{self.operand}'
