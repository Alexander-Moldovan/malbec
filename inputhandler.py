from textfile import TextFile

ASSEMBLER_ONLY          = '-a'
LINKER_ONLY             = '-l'
NO_INTERMEDIATE_FILES   = '-x'

_NO_FILES     = 0
_FILES_OPENED = 1
_NOT_FOUND    = 2
_INVALID_FILE = 3

class InputHandler(object):
    def __init__(self) -> None:
        self.state = _NO_FILES
        self.input_files = []
    
    def open_files(self, filenames : list[str], option = None) -> list:
        for name in filenames:
            newfile = TextFile()
            if '.' in name:     # File extension specified
                if   name[-4:] == '.msa' and option != LINKER_ONLY:
                    self.state = _FILES_OPENED if newfile.open_read_only_file(name) else _NOT_FOUND
                elif name[-4:] == '.mbc' and option != ASSEMBLER_ONLY:
                    self.state = _FILES_OPENED if newfile.open_read_only_file(name) else _NOT_FOUND
                else:
                    self.state = _INVALID_FILE    # ARCHIVO CON EXTENSIÓN NO VÁLIDA!
            else:               # File extension not specified
                if   option == ASSEMBLER_ONLY:
                    self.state = _FILES_OPENED if newfile.open_read_only_file(name+'.msa') else _NOT_FOUND
                elif option == LINKER_ONLY:
                    self.state = _FILES_OPENED if newfile.open_read_only_file(name+'.mbc') else _NOT_FOUND
                else:
                    self.state = _FILES_OPENED if newfile.open_read_only_file(name+'.msa') or newfile.open_read_only_file(name+'.mbc') else _NOT_FOUND
            if self.state != _FILES_OPENED:
                break

        if self.state != _FILES_OPENED:
            for file in self.input_files:
                file.close_file()
            self.input_files.clear()
        
        return self.input_files

    def close_files(self):
        for file in self.input_files:
            file.close_file()
        self.input_files.clear()
        self.state = _NO_FILES

    def get_files(self) -> list:
        return self.input_files
    
    def are_files_open(self) -> bool:
        return self.state == _FILES_OPENED
    