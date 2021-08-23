# I/O: 100
LOAD = 100
PRINT = 101
INPUT = 110

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


OPCODES = {
    "LOAD": LOAD,
    "PRINT": PRINT,
    "INPUT": INPUT,
    "INC": INC,
    "ADD": ADD,
    "SUB": SUB,
    "MUL": MUL,
    "DIV": DIV,
    "GOG": GOG,
    "GOL": GOL,
    "GOE": GOE,
    "GOTO": GOTO,
    "HALT": HALT
}


ARGS = {
    LOAD: 2,
    PRINT: 1,
    INPUT: 1,
    INC: 1,
    ADD: 3,
    SUB: 3,
    MUL: 3,
    DIV: 3,
    GOG: 3,
    GOL: 3,
    GOE: 3,
    GOTO: 1,
    HALT: 0
}
