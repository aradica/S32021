from opcodes import *


class VirtualMachine:
    def __init__(self, n_registers, p_registers):
        self.registers = n_registers * [0]
        self.n_registers = n_registers

        self.program = p_registers * [0]
        self.p_registers = p_registers
        # Pokazivač na programski registar
        self.i = 0

    def __repr__(self):
        return f"[VM] R: {self.registers}\nPROGRAM:{self.program}"

    # instrukcije
    ################################

    def LOAD(self, value, r):
        self.registers[r] = value

    def ADD(self, r1, r2, r3):
        """Stores registers[r1]+registers[r2] into registers[r3] """
        self.registers[r3] = self.registers[r1] + self.registers[r2]

    def MUL(self, r1, r2, r3):
        self.registers[r3] = self.registers[r1] * self.registers[r2]

    def DIV(self, r1, r2, r3):
        self.registers[r3] = self.registers[r1] // self.registers[r2]

    # TODO smisliti KUL imena za instrukcije (opcodove)
    def GOG(self, p, r1, r2):
        """If r1 > r2 GOTO p"""
        if self.registers[r1] > self.registers[r2]:
            self.i = p
            self.i -= 1

    def GOE(self, p, r1, r2):
        """If r1 == r2 GOTO p"""
        if self.registers[r1] == self.registers[r2]:
            self.i = p
            self.i -= 1

    def INC(self, r):
        """Increments register"""
        self.registers[r] += 1

    def PRINT(self, r):
        """Prints the value of register r"""
        print(self.registers[r])

    ###################

    def loadProgramFile(self, filename):
        """Loads raw program from file and returns list of lists(lines)"""
        with open(filename, "r") as file:
            lines = file.readlines()
            lines = [line.split() for line in lines]
        # return lines
        program = self.preprocess(lines)
        self.loadProgram(program)

    def preprocess(self, lines):
        """
        Replaces codes with numeric opcodes and
        replaces line numbers with actual indexes
        """
        program = []
        skup = set()
        i = 0
        for line in lines:
            cmd = line[0]
            skup.add(i)
            program.append(OPCODES[cmd])
            for arg in line[1:]:
                program.append(int(arg))
                i += 1
            i += 1
        i = 0
        for line in lines:
            cmd = line[0]
            if OPCODES[cmd] in [GOG, GOL, GOE]:
                # print("debug:", i, skup)
                program[i+1] = list(skup)[int(line[1])]
            i += ARGS[OPCODES[cmd]]
            i += 1
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
                # self.registers[r] = value
                self.LOAD(value, r)
                # print("value:", value)

            elif code == PRINT:
                self.i += 1
                r = self.program[self.i]
                self.PRINT(r)

            elif code == INPUT:
                self.i += 1
                r = self.program[self.i]
                value = int(input())
                self.LOAD(value, r)

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
                self.ADD(r1, -r2, r3)

            elif code == MUL:
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.MUL(r1, r2, r3)

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

            # print(code)
            # Povecat i
            self.i += 1


vm = VirtualMachine(32, 32)
vm.loadProgramFile("kod.s3")
# print(vm)
vm.run()
