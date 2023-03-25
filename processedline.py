class ProcessedLine(object):
    def __init__(self, address = 0, code = "", label = None, instruction = None, operand = None) -> None:
        self.address = address
        self.code = code
        self.set_label(label)
        self.set_instruction(instruction)
        self.set_operand(operand)

    def has_content(self):
        return (self.label != None or self.instruction != None or self.operand != None)

    def set_label(self,label:str):
        self.label = label
    def set_instruction(self,instruction:str):
        self.instruction = instruction
    def set_operand(self,operand:str):
        self.operand = operand

