from typing import Callable
from numpy import int32

class CompilerOperator(object):
    def __init__(self, symbol:str,order:int,fn: Callable,unary = False) -> None:
        self.symbol = symbol
        self.order = order
        self.fn = fn
        self.is_unary = unary

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol

    # def fn(self) -> Callable:
    #     return self._fn

    # def is_unary(self) -> bool:
    #     return self._is_unary

    # def order(self) -> int:
    #     return self._order
    
    # def symbol(self) -> str:
    #     return self._symbol
    
def is_binary_operator(token:str):
    return token in _BINARY_OPERATOR_LIST
def is_unary_operator(token:str):
    return token in _UNARY_OPERATOR_LIST
def is_variable(token:str): # TODO: corroborar mas finamente
    if len(token) == 0:
        return False
    is_string = token[0] == '\'' and token[-1] == '\''
    is_number = token[0].isnumeric() or token[0] == '$'
    is_alpha = token[0].isalpha() or token[0] in ['?','@','_']
    is_plc = token == '*'
    return is_string or is_number or is_alpha or is_plc

def get_binary_operator(token:str):
    if is_binary_operator(token):
        return _BINARY_OPERATOR_LIST[token]
    else:
        return None

def get_unary_operator(token:str):
    if is_unary_operator(token):
        return _UNARY_OPERATOR_LIST[token]
    else:
        return None


# TODO : TEST

def _fn_unary_minus(a : int32) -> list[int32,bool]:
    c = int32(-a)
    return c,c.is_integer()
def _fn_logical_not(a : int32) -> list[int32,bool]:
    c = int32(a ^ int32(0xffffffff))
    return c,c.is_integer()
def _fn_low_byte(a : int32) -> list[int32,bool]:
    c = int32(a & int32(0xff))
    return c,c.is_integer()
def _fn_high_byte(a : int32) -> list[int32,bool]:
    c = int32((a>>8) & int32(0xff))
    return c,c.is_integer()
def _fn_low_word(a : int32) -> list[int32,bool]:
    c = int32(a & int32(0xffff))
    return c,c.is_integer()
def _fn_high_word(a : int32) -> list[int32,bool]:
    c = int32((a>>16) & int32(0xffff))
    return c,c.is_integer()

def _fn_mul(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a*b)
    return c,c.is_integer()
def _fn_div(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a/b)
    return c,c.is_integer()
def _fn_mod(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a % b)
    return c,c.is_integer()
def _fn_logical_shift_right(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a >> b)
    return c,c.is_integer()
def _fn_logical_shift_left(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a << b)
    return c,c.is_integer()

def _fn_sum(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a + b)
    return c,c.is_integer()
def _fn_sub(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a - b)
    return c,c.is_integer()

def _fn_logical_and(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a & b)
    return c,c.is_integer

def _fn_logical_or(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a | b)
    return c,c.is_integer
def _fn_logical_xor(a : int32, b : int32) -> list[int32,bool]:
    c = int32(a ^ b)
    return c,c.is_integer

def _fn_equal(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a == b) else int32(0)
    return c,c.is_integer
def _fn_not_equal(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a != b) else int32(0)
    return c,c.is_integer
def _fn_greater_or_equal(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a >= b) else int32(0)
    return c,c.is_integer
def _fn_less_or_equal(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a <= b) else int32(0)
    return c,c.is_integer
def _fn_greater(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a > b) else int32(0)
    return c,c.is_integer
def _fn_less(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a < b) else int32(0)
    return c,c.is_integer
def _fn_unsigned_greater(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a+int32(-2**31) > b+int32(-2**31)) else int32(0)
    return c,c.is_integer
def _fn_unsigned_less(a : int32, b : int32) -> list[int32,bool]:
    c = int32(0xffffffff) if (a+int32(-2**31) < b+int32(-2**31)) else int32(0)
    return c,c.is_integer


_UNARY_OPERATOR_LIST = {
    '-'     : CompilerOperator('-',     1, _fn_unary_minus, True),
    '.NOT.' : CompilerOperator('.NOT.', 1, _fn_logical_not, True),
    '.LOW.' : CompilerOperator('.LOW.', 1, _fn_low_byte,    True),
    '.HIGH.': CompilerOperator('.HIGH.',1, _fn_high_byte,   True),
    '.LWRD.': CompilerOperator('.LWRD.',1, _fn_low_word,    True),
    '.HWRD.': CompilerOperator('.HWRD.',1, _fn_high_word,   True)
}

_BINARY_OPERATOR_LIST = {
    '*': CompilerOperator('*', 3, _fn_mul),
    '/': CompilerOperator('/', 3, _fn_div),
    '.MOD.': CompilerOperator('.MOD.', 3, _fn_mod),
    '.SHR.': CompilerOperator('.SHR.', 3, _fn_logical_shift_right),
    '.SHL.': CompilerOperator('.SHL.', 3, _fn_logical_shift_left),

    '+': CompilerOperator('+', 4, _fn_sum),
    '-': CompilerOperator('-', 4, _fn_sub),

    '.AND.': CompilerOperator('.AND.', 5, _fn_logical_and),
    '&'    : CompilerOperator('&',     5, _fn_logical_and),

    '.OR.' : CompilerOperator('.OR.', 6, _fn_logical_or),
    '.XOR.': CompilerOperator('.XOR.',6, _fn_logical_xor),

    '.EQ.' : CompilerOperator('.EQ.', 7, _fn_equal),
    '='    : CompilerOperator('=',    7, _fn_equal),
    '.NE.' : CompilerOperator('.NE.', 7, _fn_not_equal),
    '<>'   : CompilerOperator('<>',   7, _fn_not_equal),
    '.GE.' : CompilerOperator('.GE.', 7, _fn_greater_or_equal),
    '>='   : CompilerOperator('>='  , 7, _fn_greater_or_equal),
    '.LE.' : CompilerOperator('.LE.', 7, _fn_less_or_equal),
    '<='   : CompilerOperator('<=',   7, _fn_less_or_equal),
    '.GT.' : CompilerOperator('.GT.', 7, _fn_greater),
    '>'    : CompilerOperator('>',    7, _fn_greater),
    '.LT.' : CompilerOperator('.LT.', 7, _fn_less),
    '<'    : CompilerOperator('<',    7, _fn_less),
    '.UGT.': CompilerOperator('.UGT.',7, _fn_unsigned_greater),
    '>>'   : CompilerOperator('>>',   7, _fn_unsigned_greater),
    '.ULT.': CompilerOperator('.ULT.',7, _fn_unsigned_less),
    '<<'   : CompilerOperator('<<',   7, _fn_unsigned_less)
}

