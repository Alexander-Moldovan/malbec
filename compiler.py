from textfile import TextFile
from instruction import INSTRUCTION_SET
from directive import DIRECTIVE_SET

ADDRESS     = 0
CODE        = 1
LABEL       = 2
INSTRUCTION = 3
OPERAND     = 4

class Compiler(object):
    def __init__(self) -> None:
        pass

    def precompile(self, textfile:TextFile) -> list[list[int,str,str,str,str]]:
        precompiled = []
        error = False

        for n,line in enumerate(textfile.get_all_lines()):
            if type(line) != str or len(line) == 0:
                continue
            if line[0] == '*':
                continue
            split_line = line.split()
            precompiled_line = [0,None,None,None,None]
            if not line[0].isspace() and split_line: # starts with label
                precompiled_line[LABEL] = split_line.pop(0)
            if split_line:
                precompiled_line[INSTRUCTION] = inst = split_line.pop(0)
                if not (inst in DIRECTIVE_SET) and not (inst in INSTRUCTION_SET):
                    error = True
                    print(f'ERROR: Unknown instruction or directive {inst} in line {n+1}')
                    break
                elif (inst in DIRECTIVE_SET and DIRECTIVE_SET[inst].expects_operands()) or \
                    (inst in INSTRUCTION_SET and INSTRUCTION_SET[inst].expects_operands()):
                    if split_line:
                        precompiled_line[OPERAND] = split_line.pop(0)
                    else:
                        error = True
                        print(f'ERROR: Instruction {inst} in line {n+1} expected an operand')
                        break

            if     precompiled_line[LABEL] != None \
                or precompiled_line[INSTRUCTION] != None \
                or precompiled_line[OPERAND] != None:
                precompiled.append(precompiled_line)
        if error:
            return []
        else:
            return precompiled




        