from opcodes import OPCODES


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
        """Loads program from file"""
        with open(filename, "r") as f:
            L = f.readlines()
            kod = []
            OPCODES2 = {value: key for key, value in OPCODES.items()}
            for i in L:
                m = i.split()
                # print(m)
                for j in range(len(m)):
                    if j < 1:
                        kod.append(OPCODES2[m[j]])
                    else:
                        kod.append(m[j])
            kod = list(map(int, kod))
        return kod

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
            memo = OPCODES[code]
            if memo == "HALT":
                break
            elif memo == "LOAD":
                self.i += 1
                value = self.program[self.i]
                self.i += 1
                r = self.program[self.i]
                # self.registers[r] = value
                self.LOAD(value, r)
                # print("value:", value)

            elif memo == "PRINT":
                self.i += 1
                r = self.program[self.i]
                self.PRINT(r)

            elif memo == "INPUT":
                self.i += 1
                r = self.program[self.i]
                value = int(input())
                self.LOAD(value, r)

            elif memo == "INC":
                self.i += 1
                r = self.program[self.i]
                self.INC(r)

            elif memo == "ADD":
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.ADD(r1, r2, r3)

            elif memo == "SUB":
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.ADD(r1, -r2, r3)

            elif memo == "MUL":
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.i += 1
                r3 = self.program[self.i]
                self.MUL(r1, r2, r3)

            elif memo == "GOG":
                self.i += 1
                p = self.program[self.i]
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.GOG(p, r1, r2)

            elif memo == "GOL":
                self.i += 1
                p = self.program[self.i]
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.GOG(p, r2, r1)

            elif memo == "GOE":
                self.i += 1
                p = self.program[self.i]
                self.i += 1
                r1 = self.program[self.i]
                self.i += 1
                r2 = self.program[self.i]
                self.GOE(p, r1, r2)

            # print(memo)
            # Povecat i
            self.i += 1


vm = VirtualMachine(32, 32)
# program = [0, 2, 0, 0, 3, 1, 1, 0, 1, 2, 4, 2, 5]
program = vm.loadProgramFile("kod.s3")
vm.loadProgram(program)
print(vm)
# vm.loadProgram(program)
vm.run()
# print(vm)
