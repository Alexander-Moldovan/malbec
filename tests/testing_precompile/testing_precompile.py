from compiler import Compiler
from textfile import TextFile

c = Compiler()
tf = TextFile('_testfile0.msa')

with open('output.txt','w') as out:
#    out.write(f'{c.precompile(tf)}')
    precompiled = c.precompile(tf)
    for line in precompiled:
        out.write(f'{line}\n')
