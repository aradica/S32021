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
        rawProgram, lineSet = self.initialRead(lines)
        endpointsOuter, numDefs, endpointsDict = self.preprocessDef(lines, lineSet)
        DEFS = self.copyDef(endpointsOuter,  numDefs, rawProgram)
        program = self.processLines(rawProgram, lines, lineSet)

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
        
        proList = self.proList(rawNewProgram)
        endpoints, numDefs = self.processDef(rawNewProgram)
        DEFS = self.copyDef(endpoints, numDefs, rawNewProgram)
        newProgram = self.processLines(rawNewProgram, proList)
        return newProgram, DEFS, endpoints



    def proList(self, newProgram):
        '''
        Makes a list of all the places new lines begin
        '''
        lineSet = set()
        i = 0
        while i != len(newProgram):
            cmd = newProgram[i]
            lineSet.add(i)
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
            return endpoints, len(endpoints)
        return None, None 

    def copyDef(self, endpoints, numDefs, rawNewProgram):
        '''
        Creates a new program for function virtual machine
        Copies from program
        '''
        DEFS = {}
        if numDefs:
            for i in range(numDefs):
                funcProgram = []
                startR = endpoints[i][0]
                endR = endpoints[i][1]
                funcProgram.append(rawNewProgram[startR : endR+1])
                DEFS.update({i : funcProgram[0]})
            return DEFS
        return None


if __name__ == "__main__":
    newProgram = [420, 0, 100, 1, 0, 101, 0, 200, 0, 100, 1, 1, 301, 2, 0, 1, 421]
    processorFunct = PreprocessorFunct()
    newProgramm, DEFS, endpoints = processorFunct.process(newProgram)
    print(f'ENDPOINTS: {endpoints}\nNEWPROGRAM: {newProgram}\nDEFS: {DEFS}')
    


