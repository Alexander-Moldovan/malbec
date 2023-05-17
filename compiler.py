from textfile import TextFile
from instruction import INSTRUCTION_SET
from directive import DIRECTIVE_SET
from processedline import ProcessedLine
from numpy import int32,int16,int8

from addressingmodes import *


def precompile(textfile:TextFile) -> list[ProcessedLine]:
    precompiled = []
    error = False

    for n,line in enumerate(textfile.get_all_lines()):
        if type(line) != str or len(line) == 0:
            continue
        if line[0] == '*':
            continue
        split_line = line.split()
        precompiled_line = ProcessedLine(n+1,line)#[0,None,None,None,None]
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
                    relative_operand = False
                    if inst in INSTRUCTION_SET:
                        relative_operand = INSTRUCTION_SET[inst].is_relative()
                    precompiled_line.set_operand(split_line.pop(0),relative_operand)

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

# TODO: agregar "linea" para señalar en q linea se genero el error
def compile(precompiled : list[ProcessedLine]) -> list[dict[str,int32],bool]:
    UNKNOWN = None

    variable_list = {}
    error = False
    last_org = int32(0) # or None # NOTA: el compilador antiguo utiliza variables de 32 bits, incluso para los address
    # TODO: presentar alarmas de otro modo, ej: si last_org o offset-from org tienen overflow
    offset_from_org = int32(0)     # NOTA: considera tambien a los RMB como "ORG"s

    #precompiled = [processed_line for processed_line in precompiled if processed_line.instruction != None]

    # TODO: hacer una funcion q haga esto en lugar de utilizar esta tecnica
    for processed_line in reversed(precompiled):
        if processed_line.instruction == None and processed_line.label == None:
            precompiled.remove(processed_line)

    for processed_line in precompiled:
        label = processed_line.label
        instruction = processed_line.instruction
        operand = processed_line.operand

        if label != None and (instruction == None or (instruction.upper != 'EQU' and instruction.upper != 'ORG')) and last_org != None:
            variable_list[label] = int32(last_org + offset_from_org)   

        if instruction in DIRECTIVE_SET:
            if instruction.upper() == 'ORG':
                if operand.check_addressing_mode(EXT):
                    processed_line.addmode = EXT
                    evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
                    if error:   break
                    if evaluated:
                        ops,evaluated,error = operand.get_32bit_operand()
                        if not evaluated or error:
                            error = True
                            break
                        last_org = ops
                        if label != None:
                            variable_list[label] = ops
                    else:
                        last_org = None
                else:
                    error = True
                    break
                offset_from_org = int32(0)
            elif instruction.upper() == 'EQU':
                if label == None:
                    error = True
                    break
                if operand.check_addressing_mode(EXT):
                    processed_line.addmode = EXT
                    evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
                    if error:   break
                    if evaluated:
                        ops,evaluated,error = operand.get_32bit_operand()
                        if not evaluated or error:
                            error = True
                            break
                        variable_list[label] = ops
                    else:
                        pass # Do nothing
                else:
                    error = True
                    break
            elif instruction.upper() == 'P68H11': # TODO: hacer?
                pass
            elif instruction.upper() == 'END':  # TODO: hacer
                pass
            elif instruction.upper() == 'RMB':
                if operand.check_addressing_mode(EXT):
                    processed_line.addmode = EXT
                    evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
                    if error:   break
                    if evaluated:
                        ops,evaluated,error = operand.get_32bit_operand()
                        if not evaluated or error:
                            error = True
                            break
                        if last_org != None:
                            last_org = int32(last_org + offset_from_org + ops)
                        else:
                            last_org = None  # Redundante, pero por claridad
                    else:
                        last_org = None
                else:
                    error = True
                    break
                offset_from_org = int32(0)
            elif instruction.upper() == 'FCB':
                if operand.check_only_regular_expressions():
                    processed_line.code = ''
                    processed_line.address = None if last_org == None else last_org + offset_from_org

                    evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
                    if error:   break
                    if evaluated:
                        exp,evaluated,error = operand.get_regular_expressions(int32(-128),int32(255),1)
                        if not evaluated or error:
                            error = True
                            break
                        processed_line.code += exp
                    else:
                        processed_line.code += 'XX'*operand.get_ammount_of_expressions()

                    offset_from_org += int32((operand.get_ammount_of_expressions()) & int32(-1))

                else:
                    error = True
                    break

            elif instruction.upper() == 'FDB':
                if operand.check_only_regular_expressions():
                    processed_line.code = ''
                    processed_line.address = None if last_org == None else last_org + offset_from_org

                    evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
                    if error:   break
                    if evaluated:
                        exp,evaluated,error = operand.get_regular_expressions(int32(-32768),int32(65535),2)
                        if not evaluated or error:
                            error = True
                            break
                        processed_line.code += exp
                    else:
                        processed_line.code += 'XX'*(2*operand.get_ammount_of_expressions())

                    offset_from_org += int32((operand.get_ammount_of_expressions()*2) & int32(-1))

                else:
                    error = True
                    break

            elif instruction.upper() == 'FCC':
                if operand.check_single_string():
                    processed_line.code = ''
                    processed_line.address = None if last_org == None else last_org + offset_from_org

                    string,error = operand.get_single_string()
                    if error:
                        break
                    processed_line.code += string
                    
                else:
                    error = True
                    break


        elif instruction in INSTRUCTION_SET: 
            # TODO: ademas, evitar que crea q es dir cuando es ext, ojo
            # TODO: cambiar segun modo de direccionamiento Y CORROBORAR (recordar q la eleccion se hace ahora, para el post compilado ya va a estar definido)
            
            # Corroborar que el modo de direccionamiento sea valido
            inst = INSTRUCTION_SET[instruction]
            found_addmode = False
            for addmode in inst.opcodes:
                if operand.check_addressing_mode(addmode):
                    found_addmode = True
                    break
            if not found_addmode:
                error = True
                break
            processed_line.address = None if last_org == None else last_org + offset_from_org

            processed_line.addmode = addmode
            opcode = inst.get_opcode(addmode)
            processed_line.code = opcode
            
            evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
            if error: break
            if evaluated:
                if addmode == EXT and DIR in inst.opcodes and operand.is_value_direct():
                    addmode = DIR
                    processed_line.addmode = addmode
                    opcode = inst.get_opcode(addmode)
                    processed_line.code = opcode

                ops,evaluated,error = operand.get_operands(addmode)
                if not evaluated or error:
                    error = True
                    break
                processed_line.code += ops
                # hacer algo con el dato
            else:
                # no se pudo evaluar, van XX
                processed_line.code += 'XX'*OPERAND_SIZE[addmode]

            offset_from_org += int32( (OPERAND_SIZE[addmode] + (len(opcode)//2)) & int32(-1) )

        elif instruction == None:
            pass # TODO : hacer algo con esto (eliminar linea ?)
        else:
            print(f'ERROR: invalid instruction {instruction}')
            error = True
            break

    return variable_list if not error else {}, error
        