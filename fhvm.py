"""
'Full House' Virtual Machine

Summer School of Science
Project: Turing Complete
Višnjan, 2021
"""
from opcodes import *
import argparse


DEBUG = False


class VirtualMachine:
    def __init__(self, n_registers, p_registers):
        self.registers = n_registers * [0]
        self.n_registers = n_registers

        self.program = p_registers * [0]
        self.p_registers = p_registers
        # Pokazivač na programski registar
        self.i = 0
        self.vars = {}

    def __repr__(self):
        return f"[VM] R: {self.registers}\nP:{self.program}"

    # instrukcije
    ################################

    def LOAD(self, value, r):
        self.registers[r] = value

    def LOADP(self, value, r):
        """Loads value into location pointed by r"""
        ptr = self.registers[r]
        self.registers[ptr] = value

    def COPY(self, r1, r2):
        """Copies r1 into r2"""
        self.registers[r2] = self.registers[r1]

    def META(self, p, x):
        """Writes instruction X into p"""
        self.program[p] = x

    def ADD(self, r1, r2, r3):
        """Stores registers[r1]+registers[r2] into registers[r3] """
        self.registers[r3] = self.registers[r1] + self.registers[r2]

    def SUB(self, r1, r2, r3):
        """Stores registers[r1]-registers[r2] into registers[r3] """
        self.registers[r3] = self.registers[r1] - self.registers[r2]

    def MUL(self, r1, r2, r3):
        self.registers[r3] = self.registers[r1] * self.registers[r2]

    def DIV(self, r1, r2, r3):
        self.registers[r3] = self.registers[r1] // self.registers[r2]

    def GOG(self, p, r1, r2):
        """If r1 > r2 GOTO p"""
        if self.registers[r1] > self.registers[r2]:
            self.i = p
            self.i -= 1

    def GOE(self, p, r1, r2):
        """If r1 == r2 GOTO p"""
        if self.registers[r1] == self.registers[r2]:
            self.i = p
            # run loop increments automatically so we subtract 1
            self.i -= 1

    def GOTO(self, p):
        """Unconditional GOTO p"""
        self.i = p
        # run loop increments automatically so we subtract 1
        self.i -= 1

    def INC(self, r):
        """Increments register r"""
        self.registers[r] += 1

    def PRINT(self, r):
        """Prints the value of register r"""
        print(">>>", self.registers[r])

    def CALL(self, fname, regPointer, npointers, nargs): #TODO dovrsi ig
        newProgram = self.p_registers * [0]

        self.defs[fname]
        f = VirtualMachine(self.n_registers, self.p_registers)
        f.preprocess(newProgram)
        f.loadProgram(newProgram)

    ###################

    def loadProgramFile(self, filename):
        """Loads raw program from file and returns list of lists(lines)"""
        with open(filename, "r") as file:
            lines = file.readlines()
            lines = [line.split(";")[0].split() for line in lines]
        # print(lines)
        # return lines
        if DEBUG:
            print("[DEBUG]", lines)
        program = self.preprocess(lines)
        self.loadProgram(program)

    def preprocessDefs(self, lines):
        defs = []
        enddefs = []
        for i, line in enumerate(lines):
            if line[0] == "DEF":
                defs.append(i)
            elif line[0] == "ENDDEF":
                enddefs.append(i)

        return [(d, e) for d, e in zip(defs, reversed(enddefs))]

    def copyDef(self, endpoints):
        newProgram =  self.p_registers
        newProgram.append()

    def preprocess(self, lines):
        """
        Replaces codes with numeric opcodes and
        replaces line numbers with actual indexes
        """
        program = []
        lineSet = set()
        i = 0
        for line in lines:
            cmd = line[0]
            lineSet.add(i)
            program.append(OPCODES[cmd])
            if(line[0] == "LIST"):
                for h in range(int(line[2])):
                    self.vars[line[1] + str(h)] = len(self.vars)
                continue
            for arg in line[1:]:
                if arg < 'A':
                    program.append(int(arg))
                elif("[" in arg):
                    var = ""
                    for h in arg:
                        name = ""
                        for k in arg:
                            if(k == "["):
                                break
                            name += k
                        if(h in [str(g) for g in range(10)]):
                            var += h
                    program.append(self.vars[name+var])
                elif (arg >= 'A' and arg <= 'Z' or arg >= 'a' and arg <= 'z'):
                    if arg not in self.vars:
                        self.vars[arg] = len(self.vars)
                        program.append(self.vars[arg])
                    else:
                        program.append(self.vars[arg])
                else:
                    print("Error: Incorrect Input Value")
                i += 1
            i += 1
        i = 0
        for line in lines:
            cmd = line[0]
            if OPCODES[cmd] in [GOG, GOL, GOE, GOTO]:
                proSet = sorted(list(lineSet))
                #print("debug:", proSet, program, line)
                program[i+1] = proSet[int(line[1])-1]
            i += ARGS[OPCODES[cmd]]
            i += 1
        i = 0
        # for line in lines:
        #     cmd = line[0]
            
        #     if OPCODES[cmd] in [DEF]: #TODO dodaj DEF u OPCODES
        #         endpoints = program.preprocessDefs()
        #         newProgram = program.copyDef(endpoints)
        #     i += 1
        if DEBUG:
            print("[DEBUG]", program)
        return program

    def loadProgram(self, program):
        if len(program) > self.p_registers:
            print("Error: Program too big!")
            return None
        i = 0
        for p in program:
            self.program[i] = p
            i += 1

    def run(self):
        """Runs the current program"""
        print("===RUN===")
        while True:
            # Trenutna instrukcija ili argument
            code = self.program[self.i]
            # print(self.i, "CODE:", code)
            # code = OPCODES[code]
            if code == HALT:
                break
            elif code == LOAD:
                self.i += 1
                value = self.program[self.i]
                self.i += 1
                r = self.program[self.i]
                self.LOAD(value, r)

            elif code == LOADP:
                self.i += 1
                value = self.program[self.i]
                self.i += 1
                r = self.program[self.i]
                self.LOAD(value, self.registers[r])

            elif code == PRINT:
                self.i += 1
                r = self.program[self.i]
                self.PRINT(r)

            elif code == INPUT:
                self.i += 1
                r = self.program[self.i]
                value = int(input("<<< "))
                self.LOAD(value, r)

            elif code == INPUTP:
                self.i += 1
                r = self.program[self.i]
                value = int(input("<<< "))
                self.LOAD(value, self.registers[r])

            elif code == COPY:
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.COPY(r1, r2)

            elif code == INC:
                self.i += 1
                r = self.program[self.i]
                self.INC(r)

            elif code == ADD:
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.ADD(r1, r2, r3)

            elif code == SUB:
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.SUB(r1, r2, r3)

            elif code == MUL:
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.MUL(r1, r2, r3)

            elif code == DIV:
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.DIV(r1, r2, r3)

            elif code == GOG:
                self.i += 1
                p = self.program[self.i]
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.GOG(p, r1, r2)

            elif code == GOL:
                self.i += 1
                p = self.program[self.i]
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.GOG(p, r2, r1)

            elif code == GOE:
                self.i += 1
                p = self.program[self.i]
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.GOE(p, r1, r2)

            elif code == GOTO:
                self.i += 1
                p = self.program[self.i]
                self.GOTO(p)

            elif code == META:
                self.i += 1
                p = self.program[self.i]
                self.i += 1
                x = self.program[self.i]
                self.META(p, x)

            elif code == NOP:
                # do nothing
                self.i += 1
            
            elif(code == LIST):
                pass

            else:
                print(f"Error! Unknown instruction: '{code}'")
                break

            # Automatically goes to the next instruction
            self.i += 1
        print("===END===")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Virtual Machine")
    parser.add_argument("file", type=str,
                        help="Name of code file (.s3)")

    parser.add_argument("--registers", type=int, default=64,
                        help="Number of registers")
    parser.add_argument("--maxprogram", type=int,
                        default=64, help="Maximum program size")
    args = parser.parse_args()

    args.file
    args.registers

    vm = VirtualMachine(args.registers, args.maxprogram)
    vm.loadProgramFile(args.file)
    vm.run()
