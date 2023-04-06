from commandlineoptions import * 

_NO_FILE     = 0
_FILE_OPENED = 1
_NOT_FOUND   = 2
#_ERROR       = 3

class TextFile(object):
    def __init__(self, filename = None) -> None:
        self.state = _NO_FILE
        self.file = None
        self.name = ''
        if filename != None:
            self.open_read_only_file(filename)

    def open_read_only_file(self,filename : str) -> bool:
        self.close_file()
        try:
            self.file = open(filename, "r")
            self.state = _FILE_OPENED
            self.name = filename
        except:
            self.file = None
            self.state = _NOT_FOUND
            self.name = filename
        return self.state == _FILE_OPENED

    def close_file(self):
        if self.file != None:
            self.file.close()
        self.file = None
        self.state = _NO_FILE
        self.name = ''

    def get_all_content(self) -> str:
        if self.state == _FILE_OPENED and self.file != None:
            self.file.seek(0)
            return self.file.read()
        else:
            return ""
    
    def get_all_lines(self) -> list[str]:
        if self.state == _FILE_OPENED and self.file != None:
            self.file.seek(0)
            return self.file.readlines()
        else:
            return []       
    
    def get_next_line(self) -> str:
        if self.state == _FILE_OPENED and self.file != None:
            return self.file.readline()
        else:
            return ""
        
    def is_open(self) -> bool:
        return self.state == _FILE_OPENED

    def get_name(self) -> str:
        return self.name
    

# class InputHandler(object):
#     def __init__(self) -> None:
#         self.state = _NO_FILES
#         self.input_files = []
    
def open_files(filenames : list[str], option = None) -> list[list[TextFile], bool]:
    # self.close_files()
    _NO_FILES     = 0
    _FILES_OPENED = 1
    _NOT_FOUND    = 2
    _INVALID_FILE = 3

    state = _NO_FILES
    input_files = []
    for name in filenames:
        newfile = TextFile()
        if '.' in name:     # File extension specified
            if   name[-4:] == '.msa' and option != LINKER_ONLY:
                state = _FILES_OPENED if newfile.open_read_only_file(name) else _NOT_FOUND
            elif name[-4:] == '.mbc' and option != ASSEMBLER_ONLY:
                state = _FILES_OPENED if newfile.open_read_only_file(name) else _NOT_FOUND
            else:
                state = _INVALID_FILE    # ARCHIVO CON EXTENSIÓN NO VÁLIDA!
        else:               # File extension not specified
            if   option == ASSEMBLER_ONLY:
                name += '.msa'
                state = _FILES_OPENED if newfile.open_read_only_file(name) else _NOT_FOUND
            elif option == LINKER_ONLY:
                name += '.mbc'
                state = _FILES_OPENED if newfile.open_read_only_file(name) else _NOT_FOUND
            else:
                state = _FILES_OPENED if newfile.open_read_only_file(name+'.msa') or newfile.open_read_only_file(name+'.mbc') else _NOT_FOUND
        if state == _FILES_OPENED:
            input_files.append(newfile)
        else:
            if state == _NOT_FOUND:
                print(f'File {name} not found!')
            elif state == _INVALID_FILE:
                print(f'File {name} not valid!')
            break

    if state != _FILES_OPENED:
        for file in input_files:
            file.close_file()
        input_files.clear()
    
    return input_files, state == _FILES_OPENED

def close_files(files : list[TextFile]): # No olvidar hacer files.clear() por afuera!
    for file in files:
        file.close_file()
    # self.input_files.clear()
    # self.state = _NO_FILES

    # def get_files(self) -> list:
    #     return self.input_files
    
    # def are_files_open(self) -> bool:
    #     return self.state == _FILES_OPENED
    