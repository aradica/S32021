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
            program, DEFS, endpoints
        
        program - list of machine instructions
        DEFS - dictionary with functions and their "names" (order of declaration)
        endpoints - begin and end locations for function declarations

        """
        with open(filename, "r") as file:
            lines = file.readlines()
    
        lines = [line.split(";")[0].split() for line in lines]
        self.argsUpdate(lines)
        rawProgram, lineSet = self.initialRead(lines)
        endpointsOuter, numDefs, endpointsDict = self.preprocessDef(lines, lineSet)
        DEFS = self.copyDef(endpointsOuter,  numDefs, rawProgram)
        program = self.processLines(rawProgram, lines, lineSet)
        print(ARGS)
        return program, DEFS, endpointsDict


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
            if cmd == 'LIST':
                for h in range(int(line[2])):
                    vars[line[1]+str(h)] = len(vars)
                continue
            for arg in line[1:]:
                if arg < 'A':
                    rawProgram.append(int(arg))
                elif "[" in arg:
                    var = ""
                    for h in arg:
                        name = ""
                        for k in arg:
                            if k == "[":
                                break
                            name += k
                        if (h in [str(g) for g in range(10)]):
                            var += h
                    rawProgram.append(vars[name+var])


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
        return rawProgram, lineSet 

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
            if OPCODES[cmd] == DEF:
                i += ARGS[(OPCODES[cmd], line[1])]
            elif OPCODES[cmd] == CALL:
                i += ARGS[(OPCODES[cmd], line[1])]
            else:
                i += ARGS[OPCODES[cmd]]
            i += 1
        return rawProgram

    def preprocessDef(self, lines, lineSet):
        """
        Finds locations in the program where declerations of functions begin and end.
        Counts the number of functions 
        Returns list of endpoints,  numDefs
        """
        defs = []
        enddefs = 0
        endpoints = []
        proList = sorted(list(lineSet))
        for i, line in enumerate(lines):
            if line[0] == "DEF":
                defs.append(i)
            elif line[0] == "ENDDEF":
                enddefs = i
                endpoints.append([defs.pop(), enddefs])

        if endpoints:
            for i, l in enumerate(endpoints):
                endpoints[i][0] = proList[l[0]]
                endpoints[i][1] = proList[l[1]]
            endpoints.sort()
            endpointsOuter = []
            n = 0
            for i, point in enumerate(endpoints):
                if point[1] > n:
                    endpointsOuter.append(point)
                    n = point[1]
            endpointsDict = {x[0]:x[1] for x in endpointsOuter}
            return endpointsOuter, len(endpointsOuter), endpointsDict
        
        return None, None, {}

    def argsUpdate(self, lines):
        n = 0 
        for i, line in enumerate(lines):
            if line[0] == "DEF":
                n = len(line) -1
                ARGS.update({(DEF, line[1]) : n})
            elif line[0] == "CALL":
                n = len(line) -1
                ARGS.update({(CALL, line[1]) : n})
                 

    
    def copyDef(self, endpointsOuter, numDefs, rawProgram):
        """
        Creates a new program for function virtual machine
        Copies from program
        """
        DEFS = {}
        if numDefs:
            for i in range(numDefs):
                newProgram = []
                startR = endpointsOuter[i][0]
                endR = endpointsOuter[i][1]
                newProgram.append(rawProgram[startR : endR+1])
                DEFS.update({rawProgram[startR+1] : newProgram[0]})
            return DEFS
        else:
            return None


class PreprocessorFunct:
    def __init__(self):
        pass

    def process(self, rawNewProgram):
        '''
        Processes function program into function virtual machine instructions
        returns:
            newProgram, DEFS, endpoints
        
        newProgram - list of machine instructions for fucntion VM
        DEFS - dictionary with functions and their "names" (order of declaration)
        endpoints - begin and end locations for function declarations
        '''
        self.argsUpdate(rawNewProgram)
        print(ARGS)
        proList = self.proList(rawNewProgram)
        endpoints, numDefs, endpointsDict = self.processDef(rawNewProgram)
        fDEFS = self.copyDef(endpoints, numDefs, rawNewProgram)
        newProgram = self.processLines(rawNewProgram, proList)
        return newProgram, fDEFS, endpointsDict



    def proList(self, newProgram):
        '''
        Makes a list of all the places new lines begin
        '''
        lineSet = set()
        i = 0
        while i != len(newProgram):
            cmd = newProgram[i]
            lineSet.add(i)
            if cmd == DEF:
                i += ARGS[(cmd, newProgram[i+1])]
            elif cmd == CALL:
                i += ARGS[(cmd, newProgram[i+1])]
            else:
                i += ARGS[cmd]  
            i += 1
        
        proList = sorted(list(lineSet))
        return proList
        
    def processLines(self, newProgram, proList):
        '''
        For commands that use line pointers 

        Turns arg from line to program location
        '''
        i = 0
        while i < len(newProgram):
            cmd = newProgram[i]
            if cmd in [GOG, GOE, GOL, GOTO]:
                newProgram[i+1] = proList[newProgram[i+1]]
            if cmd == DEF:
                i += ARGS[(cmd, newProgram[i+1])]
            elif cmd == CALL:
                i += ARGS[(cmd, newProgram[i+1])]
            else:
                i += ARGS[cmd]            
            i += 1
        return newProgram

    def processDef(self, rawNewProgram):
        '''
        Finds locations in the program where declerations of functions begin and end.
        Counts the number of functions 
        Returns list of endpoints,  numDefs
        '''
        defs = []
        enddefs = 0
        endpoints = []
        for i, chr in enumerate(rawNewProgram):
            if chr == DEF:
                defs.append(i)
            elif chr == ENDDEF:
                enddefs = i
                endpoints.append([defs.pop(), enddefs])
        endpoints.reverse()
        endpoints.remove(endpoints[0])
        if endpoints:
            endpointsDict = {x[0]:x[1] for x in endpoints}
            return endpoints, len(endpoints), endpointsDict
        return None, None, None

    def argsUpdate(self, rawNewProgram):
        n = 0
        for i, char in enumerate(rawNewProgram):
            if char == DEF:
                n += 2
                name = rawNewProgram[i+1]
                X = rawNewProgram[i+2]
                n += X
                Y = rawNewProgram[i+3+X]
                n += Y + 1
                ARGS.update({(DEF, name): n})
            if char == CALL:
                n += 2
                name = rawNewProgram[i+1]
                X = rawNewProgram[i+1]
                n += X
                ARGS.update({(CALL, name) : n})
        print('TU', ARGS)



    def copyDef(self, endpoints, numDefs, rawNewProgram):
        '''
        Creates a new program for function virtual machine
        Copies from program
        '''
        fDEFS = {}
        if numDefs:
            for i in range(numDefs):
                funcProgram = []
                startR = endpoints[i][0]
                endR = endpoints[i][1]
                funcProgram.append(rawNewProgram[startR : endR+1])
                fDEFS.update({rawNewProgram[startR + 1] : funcProgram[0]})
            return fDEFS
        return None


if __name__ == "__main__":
    newProgram = [420, 0, 1, 1, 1, 2, 100, 5, 3, 301, 5, 1, 3, 100, 1, 2, 400, 100, 0, 2, 400, 421]
    processorFunct = PreprocessorFunct()
    newProgramm, DEFS, endpoints = processorFunct.process(newProgram)
    print(f'PROGRAM: {newProgram}\n>>======================================================\nDEFS: {DEFS}\n>>======================================================\nEndpointsOuter: {endpoints} ')
    


