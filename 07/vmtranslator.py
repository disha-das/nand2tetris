import sys
import os

path = sys.argv[1]
needs_bootstrap = 0
is_dir = 0

f1 = open("temp_vm", "w")
if os.path.isdir(path):
    is_dir = 1
    for file in os.listdir(path):
        if file.endswith(".vm"):
            if (str(os.path.join(file)) == "Sys.vm"):
                needs_bootstrap = 1
            file1 = os.path.join(path,file)
            with open(file1) as f:
                for line in f:
                    if "static" in line:
                        static_op = line.split()
                        if (len(static_op) == 3 and ((static_op[0] == 'push') or (static_op[0] == 'pop'))):
                            static_op[2] = str(os.path.join(file))+"static"+static_op[2]
                            line = static_op[0] +" static " + static_op[2]+'\n'
                    f1.write(line)
    f1.close()
elif os.path.isfile(path):
    with open(path) as f:
        for line in f:
            f1.write(line)
    f1.close()
filename_asm = str(path)+".asm"
filename_asm = filename_asm.replace(".vm","")

filename = "temp_vm"
vm_file = open(filename, "r")
operations = list()

Lines = vm_file.readlines()
for line in Lines:
    line = line.split("//")[0]
    if(len(line) > 0):
        operations.append((line.strip()))

while("" in operations) : 
    operations.remove("")
    
if ("function Sys.init 0" in operations):
    needs_bootstrap = 1

import pandas as pd
func_call_table = []

df_func_call_table = pd.DataFrame(func_call_table, columns = ['Name', 'Count'])

instructions = list()

final_string = '@256\nD=A\n@SP\nM=D\n'
func_init = 'Sys.init'
func_cnt = '0'
a ='@'
func_ret = 'ret'+func_init+func_cnt
final_string = final_string+a+func_ret+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
final_string = final_string+'@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
final_string = final_string+'@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
final_string = final_string+'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
final_string = final_string+'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
final_string = final_string+'@5\nD=A\n@'+func_cnt+'\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n'
final_string = final_string+'@SP\nD=M\n@LCL\nM=D\n@'+func_init+'\n0;JMP\n('+func_ret+')\n'
if (needs_bootstrap == 1):
    instructions.append(final_string)
    
    tuplee = {'Name':func_init, 'Count':1}
    df_func_call_table = df_func_call_table.append(tuplee,ignore_index = True)
	
label_cnt = 0

for op in operations:
    opargs = op.split()
    if (opargs[0] == 'push'):
        if (len(opargs) == 3):
            if (opargs[1] == 'local'):
                opargs[1] = 'LCL'
            elif (opargs[1] == 'argument'):
                opargs[1] = 'ARG'
            elif (opargs[1] == 'this'):
                opargs[1] = 'THIS'
            elif (opargs[1] == 'that'):
                opargs[1] = 'THAT'
            elif (opargs[1] == 'static'):
                opargs[1] = '16'
            elif (opargs[1] == 'temp'):
                opargs[1] = '5'
            elif (opargs[1] == 'pointer'):
                opargs[1] = '3'                
            a = '@'
            b = opargs[2]
            c = '\nD=A\n@'
            d = opargs[1]
            e1= '\nA=D+M\nD=M\n@'
            e2= '\nA=A+D\nD=M\n@'
            f = 'SP\nA=M\nM=D\n@SP\nM=M+1\n'
            if (opargs[1] == '3'):
                final_string = a+b+c+d+e2+f
            elif (opargs[1] == '5'):
                final_string = a+b+c+d+e2+f
            elif (opargs[1] == 'constant'):
                final_string = a+b+c+f
            elif (opargs[1] == '16'):
                final_string = "@"+opargs[2]+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            else:
                final_string = a+b+c+d+e1+f
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'pop'):
        if (len(opargs) == 3):
            if (opargs[1] == 'local'):
                opargs[1] = 'LCL'
            elif (opargs[1] == 'argument'):
                opargs[1] = 'ARG'
            elif (opargs[1] == 'this'):
                opargs[1] = 'THIS'
            elif (opargs[1] == 'that'):
                opargs[1] = 'THAT'
            elif (opargs[1] == 'static'):
                opargs[1] = '16'
            elif (opargs[1] == 'temp'):
                opargs[1] = '5'
            elif (opargs[1] == 'pointer'):
                opargs[1] = '3'
            a = '@'
            b = opargs[2]
            c = '\nD=A\n@'
            d = opargs[1]
            e1 = '\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'
            e2 = '\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'
            if (opargs[1] == '3'):
                final_string = a+b+c+d+e2
            elif (opargs[1] == '5'):
                final_string = a+b+c+d+e2
            elif (opargs[1] == '16'):
                final_string = "@"+opargs[2]+'\nD=A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
            else:
                final_string = a+b+c+d+e1
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'add'):
        if (len(opargs) == 1):
            final_string = '@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=D+M\n@SP\nM=M-1\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'sub'):
        if (len(opargs) == 1):
            final_string = '@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=M-D\n@SP\nM=M-1\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'neg'):
        if (len(opargs) == 1):
            final_string = '@SP\nA=M\nA=A-1\nM=-M\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'and'):
        if (len(opargs) == 1):
            final_string = '@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=D&M\n@SP\nM=M-1\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'or'):
        if (len(opargs) == 1):
            final_string = '@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=D|M\n@SP\nM=M-1\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'not'):
        if (len(opargs) == 1):
            final_string = '@SP\nA=M\nA=A-1\nM=!M\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'gt'):
        if (len(opargs) == 1):
            label_a = 'label'+str(label_cnt)
            label_cnt = label_cnt + 1
            label_b = 'label'+str(label_cnt)
            label_cnt = label_cnt + 1
            a = '@SP\nA=M\nA=A-1\nD=M\nA=A-1\nD=M-D\n@'
            b = label_a
            c = '\nD;JGT\nD=0\n@'
            d = label_b
            e = '\n0;JMP\n('
            f = label_a
            g = ')\nD=-1\n('
            h = label_b
            i = ')\n@SP\nM=M-1\nA=M\nA=A-1\nM=D\n'
            final_string = a+b+c+d+e+f+g+h+i
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'lt'):
        if (len(opargs) == 1):
            label_a = 'label'+str(label_cnt)
            label_cnt = label_cnt + 1
            label_b = 'label'+str(label_cnt)
            label_cnt = label_cnt + 1
            a = '@SP\nA=M\nA=A-1\nD=M\nA=A-1\nD=M-D\n@'
            b = label_a
            c = '\nD;JLT\nD=0\n@'
            d = label_b
            e = '\n0;JMP\n('
            f = label_a
            g = ')\nD=-1\n('
            h = label_b
            i = ')\n@SP\nM=M-1\nA=M\nA=A-1\nM=D\n'
            final_string = a+b+c+d+e+f+g+h+i
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'eq'):
        if (len(opargs) == 1):
            label_a = 'label'+str(label_cnt)
            label_cnt = label_cnt + 1
            label_b = 'label'+str(label_cnt)
            label_cnt = label_cnt + 1
            a = '@SP\nA=M\nA=A-1\nD=M\nA=A-1\nD=M-D\n@'
            b = label_a
            c = '\nD;JEQ\nD=0\n@'
            d = label_b
            e = '\n0;JMP\n('
            f = label_a
            g = ')\nD=-1\n('
            h = label_b
            i = ')\n@SP\nM=M-1\nA=M\nA=A-1\nM=D\n'
            final_string = a+b+c+d+e+f+g+h+i
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'goto'):
        if (len(opargs) == 2):
            final_string = '@'+opargs[1]+'\n0;JMP\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'label'):
        if (len(opargs) == 2):
            final_string = '('+opargs[1]+')\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'if-goto'):
        if (len(opargs) == 2):
            final_string = '@SP\nM=M-1\nA=M\nD=M\n@'+opargs[1]+'\nD;JNE\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'call'):
        if (len(opargs) == 3):
            func_name = opargs[1]
            func_cnt = 0
            if((func_name in df_func_call_table['Name'].tolist()) == False):
                tuplee = {'Name':func_name, 'Count':1}
                df_func_call_table = df_func_call_table.append(tuplee,ignore_index = True)
            if((func_name in df_func_call_table['Name'].tolist()) == True):
                for index, row in df_func_call_table.iterrows():
                    if (row["Name"] == func_name):
                        row["Count"] = row["Count"] + 1
                        func_cnt = row["Count"]
            a = '@'
            func_ret = 'ret'+func_name+str(func_cnt)
            final_string = a+func_ret+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            final_string = final_string+'@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            final_string = final_string+'@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            final_string = final_string+'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            final_string = final_string+'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            final_string = final_string+'@5\nD=A\n@'+str(int(opargs[2]))+'\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n'
            final_string = final_string+'@SP\nD=M\n@LCL\nM=D\n@'+func_name+'\n0;JMP\n('+func_ret+')\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'function'):
        if (len(opargs) == 3):
            final_string = '('+opargs[1]+')\n'
            for no_of_locals in range(int(opargs[2])):
                final_string = final_string + 'D=0\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            instructions.append(final_string)
        else:
            operations.remove(op)
    if (opargs[0] == 'return'):
        if (len(opargs) == 1):
            frm = 'R13'
            ret = 'R14'
            offset = 1
            a = '@LCL\nD=M\n@'+frm+'\nM=D\n@'+frm+'\nD=M\n@5\nD=D-A\nA=D\nD=M\n@'+ret+'\nM=D\n'
            b = '@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n'
            c = ''
            for address in ['@THAT', '@THIS', '@ARG', '@LCL']:
                c = c+'@'+frm+'\nD=M\n@'+str(offset)+'\nD=D-A\nA=D\nD=M\n'+address+'\nM=D\n'
                offset = offset + 1
            d = '@'+ret+'\nA=M\n0;JMP\n'
            final_string = a+b+c+d
            instructions.append(final_string)
        else:
            operations.remove(op)

if os.path.exists(filename):
    vm_file.close()
    os.remove(filename)

asm_file_name = filename_asm
if (is_dir == 1):
    os.chdir(path)
open(asm_file_name, 'w').close()
file_asm = open(asm_file_name,"a")
for inst in instructions:
    file_asm.write(inst)
    file_asm.write("\n")
file_asm.close()
if (is_dir == 1):
    os.chdir('..')
