#from compiler import Compiler
from compiler import precompile, compile,check_evaluation, postcompile, processed_lines_to_blocks_of_data,blocks_of_data_to_s19
from textfile import TextFile
from numpy import uint32

#c = Compiler()

n = 1
input_file_name = 'test23.msa' #f'_testfile{n}.msa'

tf = TextFile(input_file_name)

# with open(f'output{n}.txt','w') as out:
with open(f'output_test0001.txt','w') as out:
#    out.write(f'{c.precompile(tf)}')
    precompiled = precompile(tf)
    varlist,error = compile(precompiled)
    if not error:
        finished,error = postcompile(precompiled,varlist,10)
        out.write(f'POST COMPILATION\n')
        out.write(f'FINISHED = {finished}\n')

        if finished and not error:
            data,error = processed_lines_to_blocks_of_data(precompiled)
            print(f'ERROR = {error}')
            print(data)
            if not error:
                s19_file,error = blocks_of_data_to_s19(data,input_file_name[:-4])
                for line in s19_file:
                    print(line)
        else:
            print(f'FINISHED = {finished}')
            print(f'ERROR = {error}')
    else:
        out.write(f'FIRST COMPILATION\n')

    out.write(f'ERROR = {error}\n')
    for var in varlist:
        out.write(f'{var :>20} = {uint32(varlist[var]) :08X} = {varlist[var]}\n ')
    out.write('\n')
    for line in precompiled:
        out.write(f'{line}\n')
    evaluated = check_evaluation(precompiled)
    #print(f'EVALUATED = {evaluated}')

input()
