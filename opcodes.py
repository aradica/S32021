# I/O: 100
LOAD = 100
PRINT = 101
LOADP = 102
INPUT = 110
INPUTP = 111
COPY = 120


# Arithmetic
INC = 200
ADD = 210
SUB = 220
MUL = 230
DIV = 240

# Jumps
GOG = 300
GOL = 301
GOE = 310
GOTO = 311

# Halt
HALT = 400
META = 401
NOP = 402

#Other
LIST = 500

OPCODES = {
    "LOAD": LOAD,
    "PRINT": PRINT,
    "LOADP": LOADP,
    "INPUT": INPUT,
    "INPUTP": INPUTP,
    "COPY": COPY,
    "INC": INC,
    "ADD": ADD,
    "SUB": SUB,
    "MUL": MUL,
    "DIV": DIV,
    "GOG": GOG,
    "GOL": GOL,
    "GOE": GOE,
    "GOTO": GOTO,
    "HALT": HALT,
    "META": META,
    "NOP": NOP,
    "LIST": LIST   
}


ARGS = {
    LOAD: 2,
    PRINT: 1,
    LOADP: 2,
    INPUT: 1,
    INPUTP: 1,
    COPY: 2,
    INC: 1,
    ADD: 3,
    SUB: 3,
    MUL: 3,
    DIV: 3,
    GOG: 3,
    GOL: 3,
    GOE: 3,
    GOTO: 1,
    HALT: 0,
    META: 2,
    NOP: 0,
    LIST: 2
}
