from inputhandler import InputHandler
from textfile import TextFile

# TODO : probar archivos no válidos entre archivos válidos

ih = InputHandler()
files = []

def testing_input_handler(n: int,filenames = [], option = None):
    global ih,files
    print(f'\nTEST {n}')
    files= ih.open_files(filenames,option)
    print(len(files))
    for tf in files:
        if type(tf) == TextFile:
            print(tf.get_name())
        else:
            print('BUG ON InputHandler OUTPUT')


testing_input_handler(1,['_testfile0.msa'])
testing_input_handler(2,['_testfile0.msa', '_testfile1.msa', '_testfile2.msa'])
testing_input_handler(3,['_testfile2.mbc'])
testing_input_handler(4,['_testfile2.mbc', '_testfile3.mbc', '_testfile4.mbc'])
testing_input_handler(5,['_testfile5.msa'])
testing_input_handler(6,['_testfile0.mbc'])
testing_input_handler(7,['_testfile4.msa'])

testing_input_handler(8,['_testfile0','_testfile1','_testfile2','_testfile3','_testfile4'])

testing_input_handler( 9,['_testfile0.msa'],'-a')
testing_input_handler(10,['_testfile0.msa'],'-l')
testing_input_handler(11,['_testfile4.mbc'],'-a')
testing_input_handler(12,['_testfile4.mbc'],'-l')

testing_input_handler(13,['_testfile0'],'-a')
testing_input_handler(14,['_testfile0'],'-l')
testing_input_handler(15,['_testfile2'],'-a')
testing_input_handler(16,['_testfile2'],'-l')
testing_input_handler(17,['_testfile4'],'-a')
testing_input_handler(18,['_testfile4'],'-l')

testing_input_handler(19,['_testfile5'])
