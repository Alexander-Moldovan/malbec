from addressingmodes import *

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
    
    def expects_operands(self) -> bool:
        return not (INH in self.opcodes)
    
    def is_relative(self) -> bool:
        return REL in self.opcodes or \
            DIR_MSK_REL in self.opcodes or \
            INDX_MSK_REL in self.opcodes or \
            INDY_MSK_REL in self.opcodes

INSTRUCTION_SET = {
    'ABA' : Instruction('ABA', {INH:'1B'}),
    'ABX' : Instruction('ABX', {INH:'3A'}),
    'ABY' : Instruction('ABY', {INH:'183A'}),
    'ADCA': Instruction('ADCA',{IMM:'89', EXT:'B9', DIR:'99', INDX:'A9', INDY:'18A9'}),
    'ADCB': Instruction('ADCB',{IMM:'C9', EXT:'F9', DIR:'D9', INDX:'E9', INDY:'18E9'}),
    'ADDA': Instruction('ADDA',{IMM:'8B', EXT:'BB', DIR:'9B', INDX:'AB', INDY:'18AB'}),
    'ADDB': Instruction('ADDB',{IMM:'CB', EXT:'FB', DIR:'DB', INDX:'EB', INDY:'18EB'}),
    'ADDD': Instruction('ADDD',{IMM16:'C3', EXT:'F3', DIR:'D3', INDX:'E3', INDY:'18E3'}),
    'ANDA': Instruction('ANDA',{IMM:'84', EXT:'B4', DIR:'94', INDX:'A4', INDY:'18A4'}),
    'ANDB': Instruction('ANDB',{IMM:'C4', EXT:'F4', DIR:'D4', INDX:'E4', INDY:'18E4'}),
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
    'BITA': Instruction('BITA',{IMM:'85', EXT:'B5', DIR:'95', INDX:'A5', INDY:'18A5'}),
    'BITB': Instruction('BITB',{IMM:'C5', EXT:'F5', DIR:'D5', INDX:'E5', INDY:'18E5'}),
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
    'CMPA': Instruction('CMPA',{IMM:'81', EXT:'B1', DIR:'91', INDX:'A1', INDY:'18A1'}),
    'CMPB': Instruction('CMPB',{IMM:'C1', EXT:'F1', DIR:'D1', INDX:'E1', INDY:'18E1'}),
    'COM' : Instruction('COM',                     {EXT:'73', INDX:'63', INDY:'1863'}),
    'COMA': Instruction('COMA',{INH:'43'}),
    'COMB': Instruction('COMB',{INH:'53'}),
    'CPD' : Instruction('CPD', {IMM16:'1A83',EXT:'1AB3',DIR:'1A93',INDX:'1AA3',INDY:'CDA3'}),
    'CPX' : Instruction('CPX', {IMM16:'8C', EXT:'BC', DIR:'9C', INDX:'AC', INDY:'CDAC'}),
    'CPY' : Instruction('CPY', {IMM16:'188C',EXT:'18BC',DIR:'189C',INDX:'1AAC',INDY:'18AC'}),
    'DAA' : Instruction('DAA', {INH:'19'}),
    'DEC' : Instruction('DEC',                     {EXT:'7A', INDX:'6A', INDY:'186A'}),
    'DECA': Instruction('DECA',{INH:'4A'}),
    'DECB': Instruction('DECB',{INH:'5A'}),

    'DES' : Instruction('DES', {INH:'34'}),
    'DEX' : Instruction('DEX', {INH:'09'}),
    'DEY' : Instruction('DEY', {INH:'1809'}),
    'EORA': Instruction('EORA',{IMM:'88', EXT:'B8', DIR:'98', INDX:'A8', INDY:'18A8'}),
    'EORB': Instruction('EORB',{IMM:'C8', EXT:'F8', DIR:'D8', INDX:'E8', INDY:'18E8'}),
    'FDIV': Instruction('FDIV',{INH:'03'}),
    'IDIV': Instruction('IDIV',{INH:'02'}),
    'INC' : Instruction('INC',                     {EXT:'7C', INDX:'6C', INDY:'186C'}),
    'INCA': Instruction('INCA',{INH:'4C'}),
    'INCB': Instruction('INCB',{INH:'5C'}),
    'INS' : Instruction('INS', {INH:'31'}),
    'INX' : Instruction('INX', {INH:'08'}),
    'INY' : Instruction('INY', {INH:'1808'}),
    'JMP' : Instruction('JMP',                     {EXT:'7E', INDX:'6E', INDY:'186E'}),
    'JSR' : Instruction('JSR',           {EXT:'BD', DIR:'9D', INDX:'AD', INDY:'18AD'}),
    'LDAA': Instruction('LDAA',{IMM:'86', EXT:'B6', DIR:'96', INDX:'A6', INDY:'18A6'}),
    'LDAB': Instruction('LDAB',{IMM:'C6', EXT:'F6', DIR:'D6', INDX:'E6', INDY:'18E6'}),
    'LDD' : Instruction('LDD', {IMM16:'CC', EXT:'FC', DIR:'DC', INDX:'EC', INDY:'18EC'}),

    'LDS' : Instruction('LDS', {IMM16:'8E', EXT:'BE', DIR:'9E', INDX:'AE', INDY:'18AE'}),
    'LDX' : Instruction('LDX', {IMM16:'CE', EXT:'FE', DIR:'DE', INDX:'EE', INDY:'CDEE'}),
    'LDY' : Instruction('LDY', {IMM16:'18CE',EXT:'18FE',DIR:'18DE',INDX:'1AEE', INDY:'18EE'}),
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
    'ORAA': Instruction('ORAA',{IMM:'8A', EXT:'BA', DIR:'9A', INDX:'AA', INDY:'18AA'}),
    'ORAB': Instruction('ORAB',{IMM:'CA', EXT:'FA', DIR:'DA', INDX:'EA', INDY:'18EA'}),

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
    'SBCA': Instruction('SBCA',{IMM:'82', EXT:'B2', DIR:'92', INDX:'A2', INDY:'18A2'}),
    'SBCB': Instruction('SBCB',{IMM:'C2', EXT:'F2', DIR:'D2', INDX:'E2', INDY:'18E2'}),
    'SEC' : Instruction('SEC', {INH:'0D'}),
    'SEI' : Instruction('SEI', {INH:'0F'}),
    'SEV' : Instruction('SEV', {INH:'0B'}),

    'STAA': Instruction('STAA',          {EXT:'B7', DIR:'97', INDX:'A7', INDY:'18A7'}),
    'STAB': Instruction('STAB',          {EXT:'F7', DIR:'D7', INDX:'E7', INDY:'18E7'}),
    'STD' : Instruction('STD',           {EXT:'FD', DIR:'DD', INDX:'ED', INDY:'18ED'}),
    'STOP': Instruction('STOP',{INH:'CF'}),
    'STS' : Instruction('STS',           {EXT:'BF', DIR:'9F', INDX:'AF', INDY:'18AF'}),
    'STX' : Instruction('STX',           {EXT:'FF', DIR:'DF', INDX:'EF', INDY:'CDEF'}),
    'STY' : Instruction('STY',           {EXT:'18FF',DIR:'18DF',INDX:'1AEF',INDY:'18EF'}),
    'SUBA': Instruction('SUBA',{IMM:'80', EXT:'B0', DIR:'90', INDX:'A0', INDY:'18A0'}),
    'SUBB': Instruction('SUBB',{IMM:'C0', EXT:'F0', DIR:'D0', INDX:'E0', INDY:'18E0'}),
    'SUBD': Instruction('SUBD',{IMM16:'83', EXT:'B3', DIR:'93', INDX:'A3', INDY:'18A3'}),
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