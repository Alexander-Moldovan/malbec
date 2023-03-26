class CompilerOperator(object):
    def __init__(self, symbol:str,order:int,fn:function,unary = False) -> None:
        self._symbol = symbol
        self._order = order
        self._fn = fn
        self._is_unary = unary

    def fn(self) -> function:
        return self._fn

    def is_unary(self) -> bool:
        return self._is_unary

    def order(self) -> int:
        return self._order
    
    def symbol(self) -> str:
        return self._symbol

# TODO
def fn_unary_minus(a):
    return a
def fn_logical_not(a):
    return a
def fn_low_byte(a):
    return a
def fn_high_byte(a):
    return a
def fn_low_word(a):
    return a
def fn_high_word(a):
    return a

def fn_mul(a,b):
    return a
def fn_div(a,b):
    return a
def fn_mod(a,b):
    return a
def fn_logical_shift_right(a,b):
    return a
def fn_logical_shift_left(a,b):
    return a

def fn_sum(a,b):
    return a
def fn_sub(a,b):
    return a

def fn_logical_and(a,b):
    return a

def fn_logical_or(a,b):
    return a
def fn_logical_xor(a,b):
    return a

def fn_equal(a,b):
    return a
def fn_not_equal(a,b):
    return a
def fn_greater_or_equal(a,b):
    return a
def fn_less_or_equal(a,b):
    return a
def fn_greater(a,b):
    return a
def fn_less(a,b):
    return a
def fn_unsigned_greater(a,b):
    return a
def fn_unsigned_less(a,b):
    return a


UNARY_OPERATOR_LIST = {
    '-'     : CompilerOperator('-',     1, fn_unary_minus, True),
    '.NOT.' : CompilerOperator('.NOT.', 1, fn_logical_not, True),
    '.LOW.' : CompilerOperator('.LOW.', 1, fn_low_byte,    True),
    '.HIGH.': CompilerOperator('.HIGH.',1, fn_high_byte,   True),
    '.LWRD.': CompilerOperator('.LWRD.',1, fn_low_word,    True),
    '.HWRD.': CompilerOperator('.HWRD.',1, fn_high_word,   True)
}

BINARY_OPERATOR_LIST = {
    '*': CompilerOperator('*', 3, fn_mul),
    '/': CompilerOperator('/', 3, fn_div),
    '.MOD.': CompilerOperator('.MOD.', 3, fn_mod),
    '.SHR.': CompilerOperator('.SHR.', 3, fn_logical_shift_right),
    '.SHL.': CompilerOperator('.SHL.', 3, fn_logical_shift_left),

    '+': CompilerOperator('+', 4, fn_sum),
    '-': CompilerOperator('-', 4, fn_sub),

    '.AND.': CompilerOperator('.AND.', 5, fn_logical_and),
    '&'    : CompilerOperator('&',     5, fn_logical_and),

    '.OR.' : CompilerOperator('.OR.', 6, fn_logical_or),
    '.XOR.': CompilerOperator('.XOR.',6, fn_logical_xor),

    '.EQ.' : CompilerOperator('.EQ.', 7, fn_equal),
    '='    : CompilerOperator('=',    7, fn_equal),
    '.NE.' : CompilerOperator('.NE.', 7, fn_not_equal),
    '<>'   : CompilerOperator('<>',   7, fn_not_equal),
    '.GE.' : CompilerOperator('.GE.', 7, fn_greater_or_equal),
    '>='   : CompilerOperator('>='  , 7, fn_greater_or_equal),
    '.LE.' : CompilerOperator('.LE.', 7, fn_less_or_equal),
    '<='   : CompilerOperator('<=',   7, fn_less_or_equal),
    '.GT.' : CompilerOperator('.GT.', 7, fn_greater),
    '>'    : CompilerOperator('>',    7, fn_greater),
    '.LT.' : CompilerOperator('.LT.', 7, fn_less),
    '<'    : CompilerOperator('<',    7, fn_less),
    '.UGT.': CompilerOperator('.UGT.',7, fn_unsigned_greater),
    '>>'   : CompilerOperator('>>',   7, fn_unsigned_greater),
    '.ULT.': CompilerOperator('.ULT.',7, fn_unsigned_less),
    '<<'   : CompilerOperator('<<',   7, fn_unsigned_less)
}

