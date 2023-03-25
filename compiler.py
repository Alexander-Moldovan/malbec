from textfile import TextFile
from instruction import INSTRUCTION_SET
from directive import DIRECTIVE_SET
from processedline import ProcessedLine

class Compiler(object):
    def __init__(self) -> None:
        pass

    def precompile(self, textfile:TextFile) -> list[ProcessedLine]:
        precompiled = []
        error = False

        for n,line in enumerate(textfile.get_all_lines()):
            if type(line) != str or len(line) == 0:
                continue
            if line[0] == '*':
                continue
            split_line = line.split()
            precompiled_line = ProcessedLine()#[0,None,None,None,None]
            if not line[0].isspace() and split_line: # starts with label
                precompiled_line.set_label(split_line.pop(0))
            if split_line:
                inst = split_line.pop(0).upper()
                precompiled_line.set_instruction(inst)
                if not (inst in DIRECTIVE_SET) and not (inst in INSTRUCTION_SET):
                    error = True
                    print(f'ERROR: Unknown instruction or directive {inst} in line {n+1}')
                    break
                elif (inst in DIRECTIVE_SET and DIRECTIVE_SET[inst].expects_operands()) or \
                    (inst in INSTRUCTION_SET and INSTRUCTION_SET[inst].expects_operands()):
                    if split_line:
                        precompiled_line.set_operand(split_line.pop(0))
                    else:
                        error = True
                        print(f'ERROR: Instruction {inst} in line {n+1} expected an operand')
                        break

            if precompiled_line.has_content():
                precompiled.append(precompiled_line)
        if error:
            return []
        else:
            return precompiled




        