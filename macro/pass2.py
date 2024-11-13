tab = '\t'
newline = '\n'

class PassTwoMacro:
    def __init__(self):
        self.mnt = {}
        self.pnt = {}
        self.kpdtab = {}
        self.mdt = []
        self.output = []
        self.outputTable = open("output.txt", "w")
        self.IC = open("intermediateCode.txt", "r")
        self.macroNameTable = open("macroNameTable.txt", "r")
        self.macroDefTable = open("macroDefTable.txt", "r")
        self.paramNameTable = open("paramNameTable.txt", "r")
        self.keywordParamDefTable = open("keyParamDefTable.txt", "r")

    def readMNT(self):
        for line in self.macroNameTable.readlines():
            line = line.strip('\n').split('\t')
            self.mnt[line[0]] = line[1:]
    
    def readPNT(self):
        for line in self.paramNameTable.readlines():
            line = line.strip('\n').split('\t')
            self.pnt[line[0]] = line[1:]
        

    def readMDT(self):
        for line in self.macroDefTable.readlines():
            line = line.strip('\n').split('\t')
            self.mdt.append(line)
    
    def readKPDTAB(self):
        lines = self.keywordParamDefTable.readlines()
        for macro in self.mnt:
            kpdtp = int(self.mnt[macro][3])
            keyParams = int(self.mnt[macro][1])
            self.kpdtab[macro] = {}
            for line in lines[kpdtp-1:kpdtp+keyParams-1]:
                line = line.strip('\n').split('\t')
                self.kpdtab[macro][line[0]] = line[1]
    
    def createAPTAB(self, params, macro):
        aptab = self.pnt[macro].copy()
        aptabcopy: list = aptab.copy()
        for index, param in enumerate(params):
            param = param.split("=")
            if len(param) > 1: # keyword
                aptab[aptabcopy.index(param[0])] = param[1]
            else: # positional
                aptab[index] = param[0]
        for index, param in enumerate(aptab):
            if param == aptabcopy[index]:
                aptab[index] = self.kpdtab[macro].get(param)
        return aptab
    
    def processDefinition(self, macro, aptab):
        mdtp = int(self.mnt[macro][2])
        mdt = self.mdt[mdtp-1:]
        for line in mdt:
            if line[0] == 'MEND':
                return
            self.output.append([line[0]])
            for placeholder in line[1:]:
                index = int(placeholder.strip(")").split(",")[1]) - 1
                self.output[-1].append(aptab[index])

    def parseFile(self):
        lines = self.IC.readlines()
        for line in lines:
            line = line.strip('\n').split('\t')
            part_1 = line[0]
            if part_1 not in self.mnt:
                self.output.append([part_1])
                continue
            part_2 = line[1].split(", ")
            # process actual parameters
            aptab = self.createAPTAB(part_2, part_1)
            self.processDefinition(part_1, aptab)
        
        for line in self.output:
            line = tab.join(line) + newline
            self.outputTable.write(line)

pass2 = PassTwoMacro()
pass2.readMNT()
pass2.readMDT()
pass2.readPNT()
pass2.readKPDTAB()
pass2.parseFile()

