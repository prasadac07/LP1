
class Mnemonics:
    def __init__(self):
        self.AD = {
            'START': 1,
            'END': 2,
            'ORIGIN': 3,
            'EQU': 4,
            'LTORG': 5
        }
        self.IS = {
            'STOP': 0,
            'ADD': 1,
            'SUB': 2,
            'MULT': 3,
            'MOVER': 4,
            'MOVEM': 5,
            'COMP': 6,
            'BC': 7,
            'DIV': 8,
            'READ': 9,
            'PRINT': 10
        }
        self.CC = {
            'LT': 1,
            'LE': 2,
            'EQ': 3,
            'GT': 4,
            'GE': 5,
            'ANY': 6
        }
        self.DL = {
            'DC': 1,
            'DS': 2
        }
        self.RG = {
            'AREG': 1,
            'BREG': 2,
            'CREG': 3,
            'DREG': 4
        }

    def getClass(self, string):
        if string in self.IS:
            return "IS"
        elif string in self.AD:
            return "AD"
        elif string in self.CC:
            return "CC"
        elif string in self.DL:
            return "DL"
        elif string in self.RG:
            return "RG"
        else:
            return ""
        
    def getMachineCode(self, string):
        if string in self.IS:
            return self.IS[string]
        elif string in self.AD:
            return self.AD[string]
        elif string in self.CC:
            return self.CC[string]
        elif string in self.DL:
            return self.DL[string]
        elif string in self.RG:
            return self.RG[string]
        else:
            return -1
        
class PassOneAssembler:
    def __init__(self):
        self.lookup = Mnemonics()
        self.location = 0
        self.prev = -1
        self.symbolTable = {}
        self.ltrTablePtr = 0
        self.ltrTableIndex = 0
        self.literalTable = {}
        self.poolTable = [0]
        self.IC = []
        self.input = open("input.txt", "r")
        self.pool = open("poolTable.txt", "w")
        self.symbol = open("symbolTable.txt", "w")
        self.literal = open("literalTable.txt", "w")
        self.ICTable = open("ICTable.txt", "w")
    
    def calculateLocation(self, string):
        if '+' in string:
            symbol, constant = string.split('+')
            return self.symbolTable[symbol] + int(constant)
        elif '-' in string:
            symbol, constant = string.split('-')
            return self.symbolTable[symbol] + int(constant)
        else:
            return self.symbolTable[string]

    def parseFile(self):
        for line in self.input.readlines():
            self.prev = self.location
            self.IC.append([])
            line = line.strip('\n')
            line = line.split('\t')
            # print(line)

            if line[0] != "":
                self.symbolTable[line[0]] = self.location
            
            if line[1] == 'START':
                self.location = int(line[2])
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.IC[-1].append(('C', int(line[2])))
            elif line[1] == 'ORIGIN':
                self.location = self.calculateLocation(line[2])
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.IC[-1].append(('C', self.location))
            elif line[1] == 'EQU':
                self.symbolTable[line[0]] = self.calculateLocation(line[2])
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.IC[-1].append(('C', self.symbolTable[line[0]]))
            elif line[1] == 'DC' or line[1] == 'DS':
                self.symbolTable[line[0]] = self.location
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.IC[-1].append(('C', int(line[2])))
                self.location += 1
            elif line[1] == 'PRINT':
                keys = list(self.symbolTable.keys()).index(line[2])
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.IC[-1].append(('S', keys))
                self.location += 1
            elif line[1] == 'READ':
                self.symbolTable[line[2]] = None
                keys = list(self.symbolTable.keys()).index(line[2])
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.IC[-1].append(('S', keys))
                self.location += 1
            elif line[1] == 'BC':
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.IC[-1].append((self.lookup.getClass(line[2]), self.lookup.getMachineCode(line[2])))
                if line[3] not in self.symbolTable:
                    self.symbolTable[line[3]] = None
                symTableIndex = list(self.symbolTable.keys()).index(line[3])
                self.IC[-1].append(('S', symTableIndex))
                self.location += 1
            elif line[1] == 'STOP':
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                self.location += 1
            elif line[1] == 'LTORG' or line[1] == 'END':
                if(line[1] == 'END'):
                    self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))
                else:
                    self.IC.pop(-1)
                for i in range(self.ltrTablePtr, len(self.literalTable)):
                    self.IC.append([])
                    self.literalTable[i][1] = self.location
                    self.IC[-1].append(('DL', 1))
                    self.IC[-1].append(('C', self.literalTable[i][0]))
                    self.IC[-1].insert(0, self.location)
                    self.location += 1
                    self.ltrTablePtr += 1
                self.poolTable.append(self.ltrTablePtr)
            else:
                # opcode
                self.IC[-1].append((self.lookup.getClass(line[1]), self.lookup.getMachineCode(line[1])))

                # operand1
                self.IC[-1].append((self.lookup.getClass(line[2]), self.lookup.getMachineCode(line[2])))

                # operand2
                if '=' in line[3]:
                    constant = line[3].strip('=').strip("'")
                    self.literalTable[self.ltrTableIndex] = [constant, None]
                    self.IC[-1].append(('L', self.ltrTableIndex))
                    self.ltrTableIndex += 1
                else:
                    if line[3] not in self.symbolTable:
                        self.symbolTable[line[3]] = None
                    symTableIndex = list(self.symbolTable.keys()).index(line[3])
                    self.IC[-1].append(('S', symTableIndex))

                self.location += 1
            if(self.prev != -1) and (self.location - 1 == self.prev) and (line[1] not in ['END', 'LTORG']):
                self.IC[-1].insert(0, self.prev)
            print(self.IC[-1])

    def printSymbolTable(self):
        tab = '\t'
        newline = '\n'
        for index, item in enumerate(self.symbolTable):
            line = str(index) + tab + str(item) + tab + str(self.symbolTable[item]) + newline
            self.symbol.write(line)
            print(line, end="")

    def printLiteralTable(self):
        tab = '\t'
        newline = '\n'
        for key, value in self.literalTable.items():
            line = str(key) + tab + str(value[0]) + tab + str(value[1]) + newline
            self.literal.write(line)
            print(line, end="")

    def printPoolTable(self):
        for item in self.poolTable:
            self.pool.write(str(item) + '\n')
            print(item)

    def printICTable(self):
        tab = '\t'
        newline = '\n'
        for line in self.IC:
            temp = ""
            if not isinstance(line[0], int):
                temp = tab
            for item in line:
                temp += str(item)
                if(line[-1] != item):
                    temp += tab
            temp += newline
            self.ICTable.write(temp)
            print(temp, end="")




pass1 = PassOneAssembler()
pass1.parseFile()
pass1.printSymbolTable()
pass1.printLiteralTable()
pass1.printPoolTable()
pass1.printICTable()
