UNDEFINED_ADDRESSING_MODE = 'Und'
INH  = 'Inh'                # ''        -
IMM  = 'Imm'                # 'ii' 
IMM16= 'I16'               # 'jjkk'    -
DIR  = 'Dir'                # 'dd'
EXT  = 'Ext'                # 'hhll'    -
INDX = 'Xin'                # 'ff'      -
INDY = 'Yin'                # 'ff'      -
REL  = 'Rel'                # 'rr'
DIR_MSK = 'DMk'             # 'ddmm'    -
INDX_MSK = 'XMk'            # 'ffmm'    -    
INDY_MSK = 'YMk'           # 'ffmm'    -
DIR_MSK_REL = 'DMR'        # 'ddmmrr' -
INDX_MSK_REL = 'XMR'       # 'ffmmrr' -
INDY_MSK_REL = 'YMR'      # 'ffmmrr' -

OPERAND_SIZE = {
    INH:    0,
    IMM:    1,
    IMM16:  2,
    DIR:    1,
    EXT:    2,
    INDX:   1,
    INDY:   1,
    REL:    1,
    DIR_MSK:    2,
    INDX_MSK:   2,
    INDY_MSK:   2,
    DIR_MSK_REL:    3,
    INDX_MSK_REL:   3,
    INDY_MSK_REL:   3
}
