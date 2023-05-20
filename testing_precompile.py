#from compiler import Compiler
from compiler import precompile, compile,check_evaluation
from textfile import TextFile
from numpy import uint32

#c = Compiler()
tf = TextFile('_testfile1.msa')

with open('output1.txt','w') as out:
#    out.write(f'{c.precompile(tf)}')
    precompiled = precompile(tf)
    varlist,error = compile(precompiled)
    out.write(f'FIRST COMPILATION\n')
    out.write(f'ERROR = {error}\n')
    for var in varlist:
        out.write(f'{var :>20} = {uint32(varlist[var]) :08X} = {varlist[var]}\n ')
    out.write('\n')
    for line in precompiled:
        out.write(f'{line}\n')
    evaluated = check_evaluation(precompiled)
    print(f'EVALUATED = {evaluated}')
