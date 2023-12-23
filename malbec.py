import sys
from compiler import precompile, compile,check_evaluation, postcompile, processed_lines_to_blocks_of_data,blocks_of_data_to_s19
from textfile import TextFile
from numpy import uint32

if len(sys.argv) < 2:
    print("FILE TO COMPILE:",end=' ')
    input_file_name = input()
    while(input_file_name == ''):
        print("FILE TO COMPILE:",end=' ')
        input_file_name = input()
else:
    input_file_name = sys.argv[1]


def output_s19_file(s19_file):
    with open(input_file_name[:-4]+'.s19','w') as out:
        for line in s19_file:
            out.write(line+'\n')


def output_rst_file(precompiled):
    with open(input_file_name[:-4]+'.rst','w') as list_file:
        for processedline in precompiled:
            #if(processedline.instruction == 'RMB')
            if len(processedline.code) > 2*4:
                pass # ASUMO QUE EXISTE UN ADDRESS DISTINTO DE NONE, DE LO CONTRARIO, NO TENDRIA SENTIDO QUE HAYA CODE
                # TODO: corroborarlo!!!
                address_int = processedline.address
                address_str = f'{address_int:04X}'
                code_remaining = processedline.code
                list_file.write(f'{address_str}    {code_remaining[:8]}'.ljust(16)+' | '+f'{processedline.source_line_number}'.rjust(4)+'    '+(f'{processedline.source_line}').expandtabs(8))
                code_remaining = code_remaining[8:]
                while code_remaining:
                    address_int += 4
                    address_str = f'{address_int:04X}'
                    list_file.write(f'{address_str}    {code_remaining[:8]}'.ljust(16)+' | \n')
                    code_remaining = code_remaining[8:]

            else:
                address = '    ' if processedline.address == None  else f'{processedline.address:04X}'
                list_file.write(f'{address}    {processedline.code}'.ljust(16)+' | '+f'{processedline.source_line_number}'.rjust(4)+'    '+(f'{processedline.source_line}').expandtabs(8))
        list_file.write('\n')


def malbec_main(input_file_name) -> bool: # return error
    tf = TextFile(input_file_name)
    if not tf.is_open():
        print(f'ERROR: couldn\'t open file {input_file_name}')
        return True
    precompiled,error = precompile(tf)
    if error:
        #print('ERROR: couldn\'t precompile O.o')
        return error
    varlist,error = compile(precompiled)
    if error:
        #print('ERROR: couldn\'t compile :(')
        return error
    finished,error = postcompile(precompiled,varlist,10)
    if not finished or error:
        #print('ERROR: couldn\'t compile >:(')
        return (not finished or error)
    data, error = processed_lines_to_blocks_of_data(precompiled)
    if error:
        #print('ERROR: counldn\'t compile T.T')
        return error
    s19_file,error = blocks_of_data_to_s19(data, input_file_name[:-4])
    if error:
        #print('ERROR: counldn\'t compile ;.;')
        return error
    
    output_s19_file(s19_file=s19_file)
    output_rst_file(precompiled=precompiled)
    return error


error = malbec_main(input_file_name)
if error:
    input("Press enter key to exit\n")

