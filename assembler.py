import sys

filename = sys.argv[1]
print(filename)
asm_file = open(filename, "r")
instructions = list()

Lines = asm_file.readlines()
for line in Lines:
    line = line.split("//")[0]
    if(len(line) > 0):
        instructions.append((line.replace(' ', '').strip()))

while("" in instructions) : 
    instructions.remove("")

#assembler pass 1
#init the symbol table
import pandas as pd
symbol_table = [['R0',0],['R1',1],['R2',2],['R3',3],['R4',4],['R5',5],['R6',6],['R7',7],['R8',8],['R9',9],['R10',10],['R11',11],
                ['R12',12],['R13',13],['R14',14],['R15',15],['SCREEN',16384], ['KBD',24576],['SP',0],['LCL',1],['ARG',2],
                ['THIS',3],['THAT',4]]
df_symbol_table = pd.DataFrame(symbol_table, columns = ['Name', 'Value'])


#pass1
label_count = 0
for inst in instructions:
    if(inst[0] == '@'):
        variable_or_label = inst[1:]
	variable_or_label = unicode(variable_or_label, "utf-8")
        if(variable_or_label.isnumeric() == False):
            if((variable_or_label in df_symbol_table['Name'].tolist()) == False):
                tuplee = {'Name':variable_or_label, 'Value':'nil'}
                df_symbol_table = df_symbol_table.append(tuplee,ignore_index = True)
    if(inst[0] == '('):
        label = inst[1:(len(inst)-1)]
        label_value = instructions.index(inst)
        if((label in df_symbol_table['Name'].tolist()) == False):
            tuplee = {'Name':label, 'Value':label_value}
            df_symbol_table = df_symbol_table.append(tuplee,ignore_index = True)
        if((label in df_symbol_table['Name'].tolist()) == True):
            for index, row in df_symbol_table.iterrows():
                if (row["Name"] == label):
                    row["Value"] = label_value - label_count
        label_count = label_count+1;
        

#fill values for variables
count = 0
for index, row in df_symbol_table.iterrows():
    if (row["Value"] == "nil"):
        count = count + 1
        row["Value"] = count + 15

for inst in instructions:
    if(inst[0] == '@'):
        symbol = inst[1:]
	symbol = unicode(symbol, "utf-8")
        if(symbol.isnumeric() == False):
            tupe = df_symbol_table.loc[df_symbol_table['Name'] == symbol]
            tuplee = tupe.to_records(index=False)
            result = list(tuplee)
            instructions[instructions.index(inst)] = "@"+ str(result[0][1])

#remove labels gotos from instructions
instructions_final = list()
for inst in instructions:
    if(inst[0] != "("):
        instructions_final.append(inst)

my_computation = {
      "0": "0101010",
      "1": "0111111",
      "-1": "0111010",
      "D": "0001100",
      "A": "0110000",
      "!D": "0001101",
      "!A": "0110001",
      "-D": "0001111",
      "D+1": "0011111",
      "A+1": "0110111",
      "D-1": "0001110",
      "A-1": "0110010",
      "D+A": "0000010",
      "D-A": "0010011",
      "A-D": "0000111",
      "D&A": "0000000",
      "D|A": "0010101",
      "M": "1110000",
      "!M": "1110001",
      "-M": "1110011",
      "M+1": "1110111",
      "M-1": "1110010",
      "D+M": "1000010",
      "D-M": "1010011",
      "M-D": "1000111",
      "D&M": "1000000",
      "D|M": "1010101",
    
      "1+D": "0011111",
      "1+A": "0110111",
      "A+D": "0000010",
      "A&D": "0000000",
      "A|D": "0010101",
      "1+M": "1110111",
      "M+D": "1000010",
      "M&D": "1000000",
      "M|D": "1010101"
}
my_dest = {
      "": "000",
      "M": "001",
      "D": "010",
      "MD": "011",
      "A": "100",
      "AM": "101",
      "AD": "110",
      "AMD": "111"
}
my_jump = {
      "": "000",
      "JGT": "001",
      "JEQ": "010",
      "JGE": "011",
      "JLT": "100",
      "JNE": "101",
      "JLE": "110",
      "JMP": "111"
}


#pass 2 assembler
for inst in instructions_final:
    if(inst[0] == '@'):
        valuee = inst[1:]
        instructions_final[instructions_final.index(inst)] = "0" + '{0:015b}'.format(int(valuee))
    elif('=' in inst):
        dest = inst.split("=")[0]
        dest_bin = my_dest[dest]
        comp = inst.split("=")[1]
        comp_bin = my_computation[comp]
        instructions_final[instructions_final.index(inst)] = "111" + comp_bin + dest_bin + "000"
    elif(';' in inst):
        comp = inst.split(";")[0]
        comp_bin = my_computation[comp]
        jump = inst.split(";")[1]
        jump_bin = my_jump[jump]
        instructions_final[instructions_final.index(inst)] = "111" + comp_bin + "000" + jump_bin

hack_file_name = filename.replace("asm","hack")
open(hack_file_name, 'w').close()
file_hack = open(hack_file_name,"a")
for inst in instructions_final:
    file_hack.write(inst)
    file_hack.write("\n")
file_hack.close()
