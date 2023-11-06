from textfile import TextFile
from instruction import INSTRUCTION_SET
from directive import DIRECTIVE_SET, OPERAND_IS_SINGLE_VARIABLE, OPERAND_IS_ARRAY_OF_REGULAR, OPERAND_IS_SINGLE_STRING
from processedline import ProcessedLine
from numpy import int32,int16,int8, uint16, uint8
from numpy import ceil

from addressingmodes import *


def precompile(textfile:TextFile) -> list[ProcessedLine]:
    precompiled = []
    error = False

    for n,line in enumerate(textfile.get_all_lines()):
        if type(line) != str:
            continue
        if len(line) == 0 or line[0] == '*':
            precompiled_line = ProcessedLine(n+1,line)
        else:
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

        #if precompiled_line.has_content():
        precompiled.append(precompiled_line)
    if error:
        return []
    else:
        return precompiled

# TODO: agregar "linea" para señalar en q linea se genero el error
def compile(precompiled : list[ProcessedLine]) -> list[dict[str,int32],bool]:
    variable_list = {}
    error = False
    last_org = int32(0) # or None # NOTA: el compilador antiguo utiliza variables de 32 bits, incluso para los address
    # TODO: presentar alarmas de otro modo, ej: si last_org o offset-from org tienen overflow
    offset_from_org = int32(0)     # NOTA: considera tambien a los RMB como "ORG"s

    #precompiled = [processed_line for processed_line in precompiled if processed_line.instruction != None]

    # TODO: hacer una funcion q haga esto en lugar de utilizar esta tecnica
    #for processed_line in reversed(precompiled):
    #    if processed_line.instruction == None and processed_line.label == None:
    #        precompiled.remove(processed_line)

    for processed_line in precompiled:
        if not processed_line.has_content():
            continue
        label = processed_line.label
        instruction = processed_line.instruction
        operand = processed_line.operand

        if label != None and (instruction == None or (instruction != 'EQU' and instruction != 'ORG')) and last_org != None:
            variable_list[label] = int32(last_org + offset_from_org)   

        if instruction in DIRECTIVE_SET:
            directive = DIRECTIVE_SET[instruction]
            if directive.label_required and label == None:
                error = True
                break
            
            processed_line.code = ''
            # !!!
            if last_org == None or ((not directive.generates_code) and (instruction != 'RMB')):
                processed_line.address = None
            else:
                processed_line.address = last_org + offset_from_org
            

            if directive.operand_type == OPERAND_IS_ARRAY_OF_REGULAR:
                check_function = operand.operand_is_array_of_regular
                get_function = operand.get_operand_array_of_regular
            elif directive.operand_type == OPERAND_IS_SINGLE_STRING:
                check_function = operand.operand_is_single_string
                get_function = operand.get_operand_single_string
            elif directive.operand_type == OPERAND_IS_SINGLE_VARIABLE:
                check_function = operand.operand_is_single_variable
                get_function = operand.get_operand_single_variable
            else:
                continue   # p68h11 or END

            error = not check_function()
            if error:
                break

            evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
            if error:
                break

            if evaluated:
                ops,evaluated,error = get_function([directive.operand_min,directive.operand_max,directive.operand_size_in_bytes])
                if not evaluated or error:
                    error = True
                    break
                if directive.generates_code:
                    processed_line.code += ops
                if directive == DIRECTIVE_SET['ORG']:
                    last_org = ops
                if directive == DIRECTIVE_SET['EQU'] or (directive == DIRECTIVE_SET['ORG'] and label != None):
                    variable_list[label] = ops
                if directive == DIRECTIVE_SET['RMB']:
                    last_org = None if last_org == None else int32(last_org + offset_from_org + ops)
                
            else:
                if directive.reset_offset:
                    last_org = None
                elif directive == DIRECTIVE_SET['FCB'] or directive == DIRECTIVE_SET['FDB']:
                    processed_line.code += 'XX'*(operand.get_ammount_of_expressions()*directive.operand_size_in_bytes)
                elif directive == DIRECTIVE_SET['FCC']:
                    error = True
                    break

            if directive.reset_offset:
                offset_from_org = int32(0)
            offset_from_org += int32(len(processed_line.code)//2) # TODO: Checkear que no sea impar!!!
# TODO: casos p68h11 y END            



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
    
    if error:
        print('ERROR IN COMPILE-TIME')

    return variable_list if not error else {}, error

# asume que no hubieron errores durante compilacion
def postcompile(compiled : list[ProcessedLine], variable_list: dict[str,int32], number_of_iterations: int) -> list[bool,bool]:
    error = False
    finished = True

    for iteration in range(number_of_iterations):

        last_org = int32(0)
        offset_from_org = int32(0)
        finished = True
        for processed_line in compiled:
            if not processed_line.has_content():
                continue
            label = processed_line.label
            instruction = processed_line.instruction
            operand = processed_line.operand

            if label != None and (instruction == None or (instruction != 'EQU' and instruction != 'ORG')) and last_org != None:
                if not label in variable_list:
                    variable_list[label] = int32(last_org + offset_from_org)
                else:
                    pass # TODO: check si se definio anteriormente para la misma linea

            if instruction in DIRECTIVE_SET:
                directive = DIRECTIVE_SET[instruction]

                # !!!
                if (directive.generates_code or (directive == DIRECTIVE_SET['RMB'])) and processed_line.address == None and last_org != None:
                    processed_line.address = last_org + offset_from_org

                if directive.operand_type == OPERAND_IS_ARRAY_OF_REGULAR:
                    get_function = operand.get_operand_array_of_regular
                elif directive.operand_type == OPERAND_IS_SINGLE_STRING:
                    get_function = operand.get_operand_single_string
                elif directive.operand_type == OPERAND_IS_SINGLE_VARIABLE:
                    get_function = operand.get_operand_single_variable
                else:
                    continue   # p68h11 or END

# TODO: Que last_org solo pueda ser None o int32
                if operand.needs_evaluation():
                    if directive == DIRECTIVE_SET['FCC']:
                        error = True
                        break
                    evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
                    if error: break
                    if evaluated:
                        ops,evaluated,error = get_function([directive.operand_min,directive.operand_max,directive.operand_size_in_bytes])
                        if not evaluated or error:
                            error = True
                            break
                        if directive.generates_code:
                            processed_line.code = ops
                        elif directive == DIRECTIVE_SET['ORG']:
                            if label != None:
                                # TODO: checkear q no este ya
                                variable_list[label] = ops
                            last_org = ops
                            offset_from_org = int32(0)
                        elif directive == DIRECTIVE_SET['EQU']:
                            # TODO: checkear que no este ya
                            variable_list[label] = ops
                        elif directive == DIRECTIVE_SET['RMB']:
                            if last_org != None:
                                last_org = int32(last_org + offset_from_org + ops)
                            else:
                                last_org = None
                            offset_from_org = int32(0)                            

                    else:
                        finished = False
                        if directive == DIRECTIVE_SET['ORG'] or directive == DIRECTIVE_SET['RMB']:
                            last_org = None
                            offset_from_org = int32(0)
                else:
                    if directive == DIRECTIVE_SET['ORG']:
                        ops,evaluated,error = get_function([directive.operand_min,directive.operand_max,directive.operand_size_in_bytes])
                        if not evaluated or error:
                            error = True
                            break
                        last_org = ops
                        offset_from_org = int32(0)
                        
                    elif directive == DIRECTIVE_SET['RMB']:
                        ops,evaluated,error = get_function([directive.operand_min,directive.operand_max,directive.operand_size_in_bytes])
                        if not evaluated or error:
                            error = True
                            break
                        if last_org != None:
                            last_org = int32(last_org + offset_from_org + ops)
                        else:
                            last_org = None
                        offset_from_org = int32(0)
                            


                offset_from_org += int32(len(processed_line.code)//2) # TODO: check paridad



            elif instruction in INSTRUCTION_SET:
                #inst = INSTRUCTION_SET[instruction]

                if processed_line.address == None and last_org != None:
                    processed_line.address = last_org + offset_from_org
                if operand.needs_evaluation():
                    evaluated,error = operand.evaluate(None if last_org == None else last_org + offset_from_org, variable_list)
                    if error: break
                    if evaluated:
                        ops,evaluated,error = operand.get_operands(processed_line.addmode)
                        if not evaluated or error:
                            error = True
                            break
                        processed_line.code = processed_line.code[:-len(ops)] + ops
                    else:
                        finished = False

                offset_from_org += int32(len(processed_line.code)//2) # TODO: check paridad

            elif instruction == None:
                pass

            else:
                print(f'ERROR: invalid instruction {instruction}')
                error = True
                break

        if error:
            break
        if finished:
            break     

    #finished = check_evaluation(compiled) if not error else False
    return finished, error

        
def check_evaluation(compiled : list[ProcessedLine]) -> bool:
    evaluated = True
    for processed_line in compiled:
        if not processed_line.has_content():
            continue
        if processed_line.operand.needs_evaluation():
            evaluated = False
            break
        inst = processed_line.instruction
        if (inst in INSTRUCTION_SET or (inst in DIRECTIVE_SET and DIRECTIVE_SET[inst].generates_code)) and \
            (processed_line.address == None or 'X' in processed_line.code):
            evaluated = False
            break

    return evaluated

def processed_lines_to_blocks_of_data(compiled : list[ProcessedLine]) -> list[list[list[uint16,str]],bool]:
    error = False
    data = []

    if check_evaluation(compiled):
        plc = uint16(0)
        current_string = [uint16(0),[]]
        data.append(current_string)
        for processed_line in compiled:
            if not processed_line.has_content():
                continue
            instruction = processed_line.instruction
            code = processed_line.code
            operand = processed_line.operand
            if instruction == 'ORG' or instruction == 'RMB':
                ops,evaluated,error = operand.get_operand_single_variable()
                if not evaluated or error:
                    error = True
                    break
                plc = uint16(ops & uint16(-1)) if instruction == 'ORG' else uint16((plc+ops) & uint16(-1))
                current_string = [plc,[]]
                data.append(current_string)
            current_string[1].append(code)
            plc = uint16((plc + (len(code)//2)) & uint16(-1))
    else:
        error = True
    
    return data if not error else [], error

def checksum(string: str) -> str:
    sum = 0
    for i in range(len(string) // 2):
        byte = string[2*i:2*(i+1)]
        sum += int(byte,16)
    
    return f'{uint8(uint8(sum) ^ uint8(-1)):02X}'[-2:]

def blocks_of_data_to_s19(data: list[list[uint16,str]], filename = '', bytes_per_line = 16) -> list[list[str],bool]:
    error = False
    output = []

    # TODO: bytes_per_line max 32

    #header = f'{filename} by Malbec'[0:32]
    header = f'{filename}'[0:32]
    first_line = 'S0'
    first_line += f'{len(header)+3 :02X}'[-2:]
    first_line += '0000'
    for c in header:
        first_line += f'{ord(c) :02X}'[-2:]
    first_line += checksum(first_line[2:])
    output.append(first_line)

    for block in data:
        plc = uint16(block[0])
        remaining = ''.join(block[1])
        if remaining == '':
            continue
        for line in range(int(ceil((len(remaining)//2)/ bytes_per_line))): # TODO: check 'paridad'
            record = 'S1'
            address = f'{plc:04X}'[-4:]
            code = remaining[:(2*bytes_per_line)]
            byte_count = f'{(len(code)//2)+3 :02X}'[-2:]
            sum = checksum(byte_count+address+code)

            output.append(record+byte_count+address+code+sum)

            plc = uint16((plc + (len(code)//2)) & uint16(-1))
            remaining = remaining[(2*bytes_per_line):]
        if remaining != '':
            error = True
            break

    last_line = 'S9030000FC'
    output.append(last_line)

    return output if not error else [], error
