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
