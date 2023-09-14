# with open('V1.0_content/testfil2.msa') as f:
#     file = f.read()
#     for c in file:
#         print(f'{(ord(c)):02X}:\t{c}')



class InputText(object):
    def __init__(self, copying = None):
        if type(copying) == InputText:
            self.lines = copying.lines.copy()
        elif type(copying) == list:
            self.lines = copying.copy()
        elif type(copying) == str:
            self.lines = copying.replace('\r\n','\n').replace('\r','\n').split('\n')
        else:
            self.lines = []
        self.arguments = []

    def append_line(self,newline):
        self.lines.append(newline)
    
    def has_remaining_lines(self) -> bool:
        return len(self.lines) != 0

    def get_next_line(self):
        if self.has_remaining_lines:
            return self.lines.pop(0)
        else:
            return ""
        
    def set_arguments(self, arguments):
        self.arguments = arguments
    def get_arguments(self):
        return self.arguments
    def get_argument(self, n):
        if n < len(self.arguments):
            return self.arguments[n]
        else:
            return ""

class compiled_line(object):
    
    pass


compiled_file = []


