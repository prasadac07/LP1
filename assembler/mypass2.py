
class PassTwoAssembler:
    def __init__(self):
        self.symbolTable = {}
        self.literalTable = {}
        self.inputSymbol = open("symbolTable.txt", "r")
        self.inputLiteral = open("literalTable.txt", "r")
        self.inputIC = open("ICTable.txt", "r")
        self.output = open("output.txt", "w")

    def parseSymbolTable(self):
        for line in self.inputSymbol.readlines():
            line = line.strip('\n').split('\t')
            self.symbolTable[int(line[0])] = int(line[2])
        print(self.symbolTable)

    def parseliteralTable(self):
        for line in self.inputLiteral.readlines():
            line = line.strip('\n').split('\t')
            self.literalTable[int(line[0])] = int(line[2])
        print(self.literalTable)

    def formatString(self, string):
        size = len(string)
        return "0"*(3-size)+string

    def parseIC(self):
        self.parseSymbolTable()
        self.parseliteralTable()

        for line in self.inputIC.readlines():
            line = line.strip('\n').split('\t')

            if line[0] == "":
                continue
            tempLine = []
            for item in line:
                item = item.strip('(').strip(')').replace("'", "").split(",")
                if len(item) > 1:
                    if item[0] == 'IS' and '0' in item[1]:
                        tempLine.append("000")
                        tempLine.append("000")
                        tempLine.append("000")
                    elif 'D' in item[0]:
                        tempLine.append("000")
                        tempLine.append("000")
                    elif 'L' == item[0]:
                        tempLine.append(str(self.literalTable[int(item[1].strip())]))
                    elif 'S' == item[0]:
                        tempLine.append(str(self.symbolTable[int(item[1].strip())]))
                    else:
                        tempLine.append(self.formatString(item[1].strip()))   
                else:
                    tempLine.append(self.formatString(item[0]))
            
            line = "\t".join(tempLine) + '\n'
            self.output.write(line)
            print(line)


pass2 = PassTwoAssembler()
pass2.parseIC()