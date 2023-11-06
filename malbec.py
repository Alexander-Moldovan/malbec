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

tf = TextFile(input_file_name)

precompiled = precompile(tf)
varlist,error = compile(precompiled)
if not error:
    finished,error = postcompile(precompiled,varlist,10)
    if finished and not error:
        data, error = processed_lines_to_blocks_of_data(precompiled)
        if not error:
            s19_file,error = blocks_of_data_to_s19(data, input_file_name[:-4])
            if not error:
                with open(input_file_name[:-4]+'.s19','w') as out:
                    for line in s19_file:
                        out.write(line+'\n')
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

            else:
                print('ERROR: counldn\'t compile ;.;')
        else:
            print('ERROR: counldn\'t compile T.T')
    else:
        print('ERROR: couldn\'t compile >:(')
else:
    print('ERROR: couldn\'t compile :(')