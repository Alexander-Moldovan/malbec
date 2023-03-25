INH  = 1
IMM  = 2
DIR  = 3
EXT  = 4
INDX = 5
INDY = 6
REL  = 7
DIR_MSK = 8
INDX_MSK = 9
INDY_MSK = 10
DIR_MSK_REL = 11
INDX_MSK_REL = 12
INDY_MSK_REL = 13

class Instruction(object):
    def __init__(self, mnemonic:str, opcodes: dict[int,str]) -> None:
        self.mnemonic = mnemonic
        self.opcodes = opcodes
    
    def get_mnemonic(self) -> str:
        return self.mnemonic
    
    def get_opcode(self, addressing_mode) -> str:
        return self.opcodes[addressing_mode]
    
    def expects_no_operands(self) -> bool:
        return INH in self.opcodes

INSTRUCTION_SET = {
    'ABA' : Instruction('ABA', {INH:'1B'}),
    'ABX' : Instruction('ABX', {INH:'3A'}),
    'ABY' : Instruction('ABY', {INH:'183A'}),
    'ADCA': Instruction('ADCA',{IMM:'89', DIR:'99', EXT:'B9', INDX:'A9', INDY:'18A9'}),
    'ADCB': Instruction('ADCB',{IMM:'C9', DIR:'D9', EXT:'F9', INDX:'E9', INDY:'18E9'}),
    'ADDA': Instruction('ADDA',{IMM:'8B', DIR:'9B', EXT:'BB', INDX:'AB', INDY:'18AB'}),
    'ADDB': Instruction('ADDB',{IMM:'CB', DIR:'DB', EXT:'FB', INDX:'EB', INDY:'18EB'}),
    'ADDD': Instruction('ADDD',{IMM:'C3', DIR:'D3', EXT:'F3', INDX:'E3', INDY:'18E3'}),
    'ANDA': Instruction('ANDA',{IMM:'84', DIR:'94', EXT:'B4', INDX:'A4', INDY:'18A4'}),
    'ANDB': Instruction('ANDB',{IMM:'C4', DIR:'D4', EXT:'F4', INDX:'E4', INDY:'18E4'}),
    'ASL' : Instruction('ASL',                     {EXT:'78', INDX:'68', INDY:'1868'}),
    'ASLA': Instruction('ASLA',{INH:'48'}),
    'ASLB': Instruction('ASLB',{INH:'58'}),
    'ASLD': Instruction('ASLD',{INH:'05'}),

    'ASR' : Instruction('ASR',                     {EXT:'77', INDX:'67', INDY:'1867'}),
    'ASRA': Instruction('ASRA',{INH:'47'}),
    'ASRB': Instruction('ARSB',{INH:'57'}),
    'BCC' : Instruction('BCC', {REL:'24'}),
    'BCLR': Instruction('BCLR',{DIR_MSK:'15',INDX_MSK:'1D',INDY_MSK:'181D'}),
    'BCS' : Instruction('BCS', {REL:'25'}),
    'BEQ' : Instruction('BEQ', {REL:'27'}),
    'BGE' : Instruction('BGE', {REL:'2C'}),
    'BGT' : Instruction('BGT', {REL:'2E'}),
    'BHI' : Instruction('BHI', {REL:'22'}),
    'BHS' : Instruction('BHS', {REL:'24'}),
    'BITA': Instruction('BITA',{IMM:'85', DIR:'95', EXT:'B5', INDX:'A5', INDY:'18A5'}),
    'BITB': Instruction('BITB',{IMM:'C5', DIR:'D5', EXT:'F5', INDX:'E5', INDY:'18E5'}),
    'BLE' : Instruction('BLE', {REL:'2F'}),
    'BLO' : Instruction('BLO', {REL:'25'}),
    'BLS' : Instruction('BLS', {REL:'23'}),
    'BLT' : Instruction('BLT', {REL:'2D'}),
    'BMI' : Instruction('BMI', {REL:'2B'}),
    'BNE' : Instruction('BNE', {REL:'26'}),
    'BPL' : Instruction('BPL', {REL:'2A'}),
    'BRA' : Instruction('BRA', {REL:'20'}),
    'BRCLR':Instruction('BRCLR',{DIR_MSK_REL:'13',INDX_MSK_REL:'1F',INDY_MSK_REL:'181F'}),
    'BRN' : Instruction('BRN', {REL:'21'}),
    'BRSET':Instruction('BRSET',{DIR_MSK_REL:'12',INDX_MSK_REL:'1E',INDY_MSK_REL:'181E'}),
    'BSET': Instruction('BSET',{DIR_MSK:'14',INDX_MSK:'1C',INDY_MSK:'181C'}),
    'BSR' : Instruction('BSR', {REL:'8D'}),
    'BVC' : Instruction('BVC', {REL:'28'}),

    'BVS' : Instruction('BVS', {REL:'29'}),
    'CBA' : Instruction('CBA', {INH:'11'}),
    'CLC' : Instruction('CLC', {INH:'0C'}),
    'CLI' : Instruction('CLI', {INH:'0E'}),
    'CLR' : Instruction('CLR',                     {EXT:'7F', INDX:'6F', INDY:'186F'}),
    'CLRA': Instruction('CLRA',{INH:'4F'}),
    'CLRB': Instruction('CLRB',{INH:'5F'}),
    'CLV' : Instruction('CLV', {INH:'0A'}),
    'CMPA': Instruction('CMPA',{IMM:'81', DIR:'91', EXT:'B1', INDX:'A1', INDY:'18A1'}),
    'CMPB': Instruction('CMPB',{IMM:'C1', DIR:'D1', EXT:'F1', INDX:'E1', INDY:'18E1'}),
    'COM' : Instruction('COM',                     {EXT:'73', INDX:'63', INDY:'1863'}),
    'COMA': Instruction('COMA',{INH:'43'}),
    'COMB': Instruction('COMB',{INH:'53'}),
    'CPD' : Instruction('CPD', {IMM:'1A83',DIR:'1A93',EXT:'1AB3',INDX:'1AA3',INDY:'CDA3'}),
    'CPX' : Instruction('CPX', {IMM:'8C', DIR:'9C', EXT:'BC', INDX:'AC', INDY:'CDAC'}),
    'CPY' : Instruction('CPY', {IMM:'188C',DIR:'189C',EXT:'18BC',INDX:'1AAC',INDY:'18AC'}),
    'DAA' : Instruction('DAA', {INH:'19'}),
    'DEC' : Instruction('DEC',                     {EXT:'7A', INDX:'6A', INDY:'186A'}),
    'DECA': Instruction('DECA',{INH:'4A'}),
    'DECB': Instruction('DECB',{INH:'5A'}),

    'DES' : Instruction('DES', {INH:'34'}),
    'DEX' : Instruction('DEX', {INH:'09'}),
    'DEY' : Instruction('DEY', {INH:'1809'}),
    'EORA': Instruction('EORA',{IMM:'88', DIR:'98', EXT:'B8', INDX:'A8', INDY:'18A8'}),
    'EORB': Instruction('EORB',{IMM:'C8', DIR:'D8', EXT:'F8', INDX:'E8', INDY:'18E8'}),
    'FDIV': Instruction('FDIV',{INH:'03'}),
    'IDIV': Instruction('IDIV',{INH:'02'}),
    'INC' : Instruction('INC',                     {EXT:'7C', INDX:'6C', INDY:'186C'}),
    'INCA': Instruction('INCA',{INH:'4C'}),
    'INCB': Instruction('INCB',{INH:'5C'}),
    'INS' : Instruction('INS', {INH:'31'}),
    'INX' : Instruction('INX', {INH:'08'}),
    'INY' : Instruction('INY', {INH:'1808'}),
    'JMP' : Instruction('JMP',                     {EXT:'7E', INDX:'6E', INDY:'186E'}),
    'JSR' : Instruction('JSR',           {DIR:'9D', EXT:'BD', INDX:'AD', INDY:'18AD'}),
    'LDAA': Instruction('LDAA',{IMM:'86', DIR:'96', EXT:'B6', INDX:'A6', INDY:'18A6'}),
    'LDAB': Instruction('LDAB',{IMM:'C6', DIR:'D6', EXT:'F6', INDX:'E6', INDY:'18E6'}),
    'LDD' : Instruction('LDD', {IMM:'CC', DIR:'DC', EXT:'FC', INDX:'EC', INDY:'18EC'}),

    'LDS' : Instruction('LDS', {IMM:'8E', DIR:'9E', EXT:'BE', INDX:'AE', INDY:'18AE'}),
    'LDX' : Instruction('LDX', {IMM:'CE', DIR:'DE', EXT:'FE', INDX:'EE', INDY:'CDEE'}),
    'LDY' : Instruction('LDY', {IMM:'18CE',DIR:'18DE',EXT:'18FE',INDX:'1AEE', INDY:'18EE'}),
    'LSL' : Instruction('LSL',                     {EXT:'78', INDX:'68', INDY:'1868'}),
    'LSLA': Instruction('LSLA',{INH:'48'}),
    'LSLB': Instruction('LSLB',{INH:'58'}),
    'LSLD': Instruction('LSLD',{INH:'05'}),
    'LSR' : Instruction('LSR',                     {EXT:'74', INDX:'64', INDY:'1864'}),
    'LSRA': Instruction('LSRA',{INH:'44'}),
    'LSRB': Instruction('LSRB',{INH:'54'}),
    'LSRD': Instruction('LSRD',{INH:'04'}),
    'MUL' : Instruction('MUL', {INH:'3D'}),
    'NEG' : Instruction('NEG',                     {EXT:'70', INDX:'60', INDY:'1860'}),
    'NEGA': Instruction('NEGA',{INH:'40'}),
    'NEGB': Instruction('NEGB',{INH:'50'}),
    'NOP' : Instruction('NOP', {INH:'01'}),
    'ORAA': Instruction('ORAA',{IMM:'8A', DIR:'9A', EXT:'BA', INDX:'AA', INDY:'18AA'}),
    'ORAB': Instruction('ORAB',{IMM:'CA', DIR:'DA', EXT:'FA', INDX:'EA', INDY:'18EA'}),

    'PSHA': Instruction('PSHA',{INH:'36'}),
    'PSHB': Instruction('PSHB',{INH:'37'}),
    'PSHX': Instruction('PSHX',{INH:'3C'}),
    'PSHY': Instruction('PSHY',{INH:'183C'}),
    'PULA': Instruction('PULA',{INH:'32'}),
    'PULB': Instruction('PULB',{INH:'33'}),
    'PULX': Instruction('PULX',{INH:'38'}),
    'PULY': Instruction('PULY',{INH:'1838'}),
    'ROL' : Instruction('ROL',                     {EXT:'79', INDX:'69', INDY:'1869'}),
    'ROLA': Instruction('ROLA',{INH:'49'}),
    'ROLB': Instruction('ROLB',{INH:'59'}),
    'ROR' : Instruction('ROR',                     {EXT:'76', INDX:'66', INDY:'1866'}),
    'RORA': Instruction('RORA',{INH:'46'}),
    'RORB': Instruction('RORB',{INH:'56'}),
    'RTI' : Instruction('RTI', {INH:'3B'}),
    'RTS' : Instruction('RTS', {INH:'39'}),
    'SBA' : Instruction('SBA', {INH:'10'}),
    'SBCA': Instruction('SBCA',{IMM:'82', DIR:'92', EXT:'B2', INDX:'A2', INDY:'18A2'}),
    'SBCB': Instruction('SBCB',{IMM:'C2', DIR:'D2', EXT:'F2', INDX:'E2', INDY:'18E2'}),
    'SEC' : Instruction('SEC', {INH:'0D'}),
    'SEI' : Instruction('SEI', {INH:'0F'}),
    'SEV' : Instruction('SEV', {INH:'0B'}),

    'STAA': Instruction('STAA',          {DIR:'97', EXT:'B7', INDX:'A7', INDY:'18A7'}),
    'STAB': Instruction('STAB',          {DIR:'D7', EXT:'F7', INDX:'E7', INDY:'18E7'}),
    'STD' : Instruction('STD',           {DIR:'DD', EXT:'FD', INDX:'ED', INDY:'18ED'}),
    'STOP': Instruction('STOP',{INH:'CF'}),
    'STS' : Instruction('STS',           {DIR:'9F', EXT:'BF', INDX:'AF', INDY:'18AF'}),
    'STX' : Instruction('STX',           {DIR:'DF', EXT:'FF', INDX:'EF', INDY:'CDEF'}),
    'STY' : Instruction('STY',           {DIR:'18DF',EXT:'18FF',INDX:'1AEF',INDY:'18EF'}),
    'SUBA': Instruction('SUBA',{IMM:'80', DIR:'90', EXT:'B0', INDX:'A0', INDY:'18A0'}),
    'SUBB': Instruction('SUBB',{IMM:'C0', DIR:'D0', EXT:'F0', INDX:'E0', INDY:'18E0'}),
    'SUBD': Instruction('SUBD',{IMM:'83', DIR:'93', EXT:'B3', INDX:'A3', INDY:'18A3'}),
    'SWI' : Instruction('SWI', {INH:'3F'}),
    'TAB' : Instruction('TAB', {INH:'16'}),
    'TAP' : Instruction('TAP', {INH:'06'}),
    'TBA' : Instruction('TBA', {INH:'17'}),
    'TEST': Instruction('TEST',{INH:'00'}),
    'TPA' : Instruction('TPA', {INH:'07'}),
    'TST' : Instruction('TST',                     {EXT:'7D', INDX:'6D', INDY:'186D'}),
    'TSTA': Instruction('TSTA',{INH:'4D'}),
    'TSTB': Instruction('TSTB',{INH:'5D'}),
    'TSX' : Instruction('TSX', {INH:'30'}),
    
    'TSY' : Instruction('TSY', {INH:'1830'}),
    'TXS' : Instruction('TXS', {INH:'35'}),
    'TYS' : Instruction('TYS', {INH:'1835'}),
    'WAI' : Instruction('WAI', {INH:'3E'}),
    'XGDX': Instruction('XGDX',{INH:'8F'}),
    'XGDY': Instruction('XGDY',{INH:'188F'})

}