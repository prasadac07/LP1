from pass1 import PassOneMacro
from pass2 import PassTwoMacro

pass1 = PassOneMacro()
pass2 = PassTwoMacro()

print("Pass1:")
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


print("\nPass2:")
pass2.readMNT()
pass2.readMDT()
pass2.readPNT()
pass2.readKPDTAB()
pass2.parseFile()
