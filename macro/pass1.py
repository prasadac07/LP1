tab = '\t'
newline = '\n'

class PassOneMacro:
    def __init__(self):
        self.macroNameTable = {}
        self.macroDefTable = []
        self.macroDefTablePtr = 1
        self.keyParamDefTable = []
        self.keyParamDefTablePtr = 1
        self.paramNameTable = {}
        self.ICPtr = 0
        self.ICOutput = open("intermediateCode.txt", "w")
        self.paramNameOutput = open("paramNameTable.txt", "w")
        self.keyParamDefOutput = open("keyParamDefTable.txt", "w")
        self.macroNameOutput = open("macroNameTable.txt", "w")
        self.macroDefOutput = open("macroDefTable.txt", "w")
        self.input = open("input.txt", "r")

    def parseFile(self):
        lines = self.input.readlines()
        currMacro = None
        inMacroDef = False
        for line in lines:
            line = line.strip('\n').split('\t')
            part_1 = line[0]
            if part_1 == 'START':
                break
            self.ICPtr += 1
            if part_1 == 'MACRO':
                inMacroDef = True
                continue
            elif inMacroDef:
                currMacro = part_1
                self.paramNameTable[currMacro] = []
                part_2 = line[1].split(", ")
                keywordParamCount = 0
                posParamCount = 0
                for param in part_2:
                    param = param.strip("&").split('=')
                    if len(param) > 1:
                        keywordParamCount += 1
                        self.keyParamDefTable.append([param[0], param[1]])
                    else:
                        posParamCount += 1
                    self.paramNameTable[currMacro].append(param[0])
                self.macroNameTable[currMacro] =  [posParamCount, keywordParamCount, self.macroDefTablePtr, 0 if keywordParamCount == 0 else self.keyParamDefTablePtr]
                self.keyParamDefTablePtr += keywordParamCount
                inMacroDef = False
            else:
                array = [part_1]
                part_2 = []
                if len(line) > 1:
                    part_2 = line[1].split(", ")
                for operand in part_2:
                    operand = operand.strip("&")
                    pnt = self.paramNameTable[currMacro]
                    temp = operand
                    if operand in pnt:
                        index = pnt.index(operand) + 1
                        temp = "({}, {})".format('P', index)
                    array.append(temp)
                self.macroDefTable.append(array)
                self.macroDefTablePtr += 1
                if part_1 == "MEND":
                    currMacro = None

    def writeICTable(self):
        self.input.seek(0)
        lines = self.input.readlines()
        for i in range(self.ICPtr, len(lines)):
            line = lines[i]
            self.ICOutput.write(line)

    def writeMacroDefTable(self):
        for item in self.macroDefTable:
            line = tab.join(item) + newline
            self.macroDefOutput.write(line)

    def writeMacroNameTable(self):
        for key, value in self.macroNameTable.items():
            line = str(key)
            for item in value:
                line += tab + str(item)
            line += newline
            self.macroNameOutput.write(line)

    def writeParamNameTable(self):
        for key, value in self.paramNameTable.items():
            line = str(key)
            for item in value:
                line += tab + str(item)
            line += newline
            self.paramNameOutput.write(line)

    def writeKeyParamDefTable(self):
        line = ""
        for name, value in self.keyParamDefTable:
            line = name + tab + value + newline
            self.keyParamDefOutput.write(line)

pass1 = PassOneMacro()
pass1.parseFile()
pass1.writeICTable()
pass1.writeMacroDefTable()
pass1.writeKeyParamDefTable()
pass1.writeMacroNameTable()
pass1.writeParamNameTable()
pass1.ICOutput.close()
pass1.macroDefOutput.close()
pass1.macroNameOutput.close()
pass1.paramNameOutput.close()
pass1.keyParamDefOutput.close()