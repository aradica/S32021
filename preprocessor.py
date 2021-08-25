#LOADPROGRAMFILE
#PREPROCESSDEF
#PREPROCESSLINES
#COPYDEF
from opcodes import *


class Preprocessor:
    def __init__(self):
        pass

    def process(self, filename):
        """
        Processes code file into virtual machine instructions
        returns:
            program, newProgram, endpoints
        
        program - list of machine instructions
        newProgram - function instructions
        endpoints - begin and end locations for function declarations

        """
        with open(filename, "r") as file:
            lines = file.readlines()
    
        lines = [line.split(";")[0].split() for line in lines]
        rawProgram, lineSet = self.initialRead(lines)
        program = self.processLines(rawProgram, lines, lineSet)
        startR, endR = self.preprocessDef(lines, lineSet)
        newProgram = self.copyDef(startR, endR, program)

        return program, newProgram, startR, endR


    def initialRead(self, lines):
        """
        Returns rawProgram which is not readable to virtual machine
        Turn variables into register locations and commands indo opcodes
        Remembers where lines start in the program instructions
        """
        vars = {}
        rawProgram = []
        lineSet = set()
        i = 0
        for line in lines:
            cmd = line[0]
            lineSet.add(i)
            rawProgram.append(OPCODES[cmd])
            for arg in line[1:]:
                if arg < 'A':
                    rawProgram.append(int(arg))
                elif arg >= 'A' and arg <= 'Z' or arg >= 'a' and arg <= 'z':
                    if arg not in vars:
                        vars[arg] = len(vars)
                        rawProgram.append(vars[arg])
                    else:
                        rawProgram.append(vars[arg])
                else:
                    print("Error: Incorrect Input Value")
                i += 1
            i += 1
        return rawProgram, lineSet #TODO DODAJ SVE OSTALO IG

    def preprocessDef(self, lines, lineSet):
        """
        Finds locations in the program where declerations of functions begin and end.
        Returns startR, endR
        """
        defs = []
        enddefs = []
        endpoints = []
        proList = sorted(list(lineSet))
        for i, line in enumerate(lines):
            if line[0] == "DEF":
                defs.append(i)
            elif line[0] == "ENDDEF":
                enddefs.append(i)

        if defs:
            endpoints =  [(d, e) for d, e in zip(defs, reversed(enddefs))]
            # Gets the first (outermost) endpoints
            startL, endL = map(int, endpoints[0])
            startR, endR = proList[startL], proList[endL]

            return startR, endR
        return None, None

    def processLines(self, rawProgram, lines, lineSet):
        """
        For commands that use line pointers 

        Turns arg from line to program location
        """
        i = 0
        proList = sorted(list(lineSet))
        for line in lines:
            cmd = line[0]
            if OPCODES[cmd] in [GOG, GOL, GOE, GOTO]:
                rawProgram[i+1] = proList[int(line[1])-1]
            i += ARGS[OPCODES[cmd]]
            i += 1
        return rawProgram
    
    def copyDef(self, startR, endR, program):
        """
        Creates a new program for function virtual machine
        Copies from program
        """
        if startR:
            newProgram = program[startR : endR+1]
            return newProgram
        return None


        
if __name__ == "__main__":
    processor = Preprocessor()
    program = processor.process("kod.s3")