import sys
import os

filename = sys.argv[1]

print(filename)
jack_file = open(filename, "r")
jack_line = list()

inside_comm = 0
Lines = jack_file.readlines()
for line in Lines:
    if (line == "/**\n"):
        inside_comm = 1
    if (line == " */\n"):
        inside_comm = 0
    if (inside_comm):
        line = "//\n"
    line = line.split("//")[0]
    line = line.split("/**")[0]
    line = line.split("/*")[0]
    line = line.split(" */")[0]
    if(len(line) > 0):
        jack_line.append((line.strip()))
        
while("" in jack_line) : 
    jack_line.remove("")


keyword_list  = ['class','constructor','function','method','field','static','var','int','char',
                 'boolean','void','true','false','null','this','let','do','if','else','while','return']
symbol_list = ['{' , '}' , '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , '-' , '*' , '/' , '&' , '|' ,
               '<' , '>' , '=' , '~']


import re

tokens = list()
tokens.append("<tokens>\n")

for jl in jack_line:
    for p in symbol_list:
        jl = jl.replace(p," "+p+" ")
    result = re.findall('"([^"]*)"', jl)
    if (result):
        index = (jl.find(result[0]))
        tks_a = jl[0:index-1]
        tks_b = jl[index-1:index+len(result[0])+1]
        tks_c = jl[index+len(result[0])+1:]
        tks = tks_a.split()
        tks.append(tks_b)
        tks = tks + tks_c.split()
    else:
        tks = jl.split()
    
    for tk in tks:
        if (tk in keyword_list):
            tokens.append(""+"<keyword> "+tk+" </keyword>\n")
        elif (tk in symbol_list):
            if (tk == "<"):
                tk = "&lt;"
            if (tk == ">"):
                tk = "&gt;"
            if (tk == "&"):
                tk = "&amp;"
            tokens.append(""+"<symbol> "+tk+" </symbol>\n")
        elif (tk.isdigit() and int(tk) >= 0 and int(tk) <= 32767):
            tokens.append(""+"<integerConstant> "+tk+" </integerConstant>\n")
        elif (re.findall('"([^"]*)"', tk)):
            tk = tk.replace('"', '')
            tokens.append(""+"<stringConstant> "+tk+" </stringConstant>\n")
        elif (re.findall('^[a-zA-Z_]+[a-zA-Z0-9_]*\w*$', tk)):
            tokens.append(""+"<identifier> "+tk+" </identifier>\n")

tokens.append("</tokens>\n")


xmlT_file_name = filename.replace(".jack","T.xml")
open(xmlT_file_name, 'w').close()
file_Txml = open(xmlT_file_name,"a")
for tok in tokens:
    file_Txml.write(tok)
file_Txml.close()


#tokens
tokens
parsed_lines = list()
curr_idx = 1
indent_len = 0


def indent_plus():
    global indent_len
    indent_len = indent_len + 2
    
def indent_minus():
    global indent_len
    indent_len = indent_len - 2
    
def print_indent():
    global indent_len
    for i in range(0, int(indent_len)):
        parsed_lines.append(" ")


def compile_expressionList():
    global curr_idx
    print_indent()
    parsed_lines.append("<expressionList>\n")
    indent_plus()
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == ")"):
        curr_idx = curr_idx - 1
        indent_minus()
        print_indent()
        parsed_lines.append("</expressionList>\n")
        return
    
    compile_expression()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    
    while (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == ","):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        compile_expression()
        tkns = tokens[curr_idx]
        tkn = tkns.split()    
    
    curr_idx = curr_idx - 1
    indent_minus()
    print_indent()
    parsed_lines.append("</expressionList>\n")


def compile_parameterList():
    global curr_idx
    print_indent()
    parsed_lines.append("<parameterList>\n")
    indent_plus()
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == ")"):
        curr_idx = curr_idx - 1
        indent_minus()
        print_indent()
        parsed_lines.append("</parameterList>\n")
        return
        
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>"):
        if (tkn[1] == "int" or tkn[1] == "char" or tkn[1] == "boolean"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected keyword "+tkns+" seen in parameterList")

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; identifier expected in parameterList ")
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    while (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == ","):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>"):
            if (tkn[1] == "int" or tkn[1] == "char" or tkn[1] == "boolean"):
                print_indent()
                parsed_lines.append(tokens[curr_idx])
            else:
                raise Exception("Unexpected keyword seen")

        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected keyword "+tkns+" seen in parameterList")
            
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
    
    curr_idx = curr_idx - 1
    indent_minus()
    print_indent()
    parsed_lines.append("</parameterList>\n")
    



def compile_term():
    global curr_idx
    print_indent()
    parsed_lines.append("<term>\n")
    indent_plus()

    tkns = tokens[curr_idx]
    tkn = tkns.split()
    
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>" and tkn[1] in ['true','false','null','this']):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    elif (tkn[0] == "<integerConstant>" and tkn[2] =="</integerConstant>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    elif (tkn[0] == "<stringConstant>" and tkn[len(tkn)-1] =="</stringConstant>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    elif (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        tkns_plus = tokens[curr_idx+1]
        tkn_plus = tkns_plus.split()
        if (tkn_plus[0] == "<symbol>" and tkn_plus[1] == "[" and tkn_plus[2] =="</symbol>"):
            curr_idx = curr_idx + 1
            tkns = tokens[curr_idx]
            tkn = tkns.split()
            print_indent()
            parsed_lines.append(tokens[curr_idx])
            curr_idx = curr_idx + 1
            tkns = tokens[curr_idx]
            tkn = tkns.split()
            compile_expression()
            
            tkns = tokens[curr_idx]
            tkn = tkns.split()
            if (tkn[0] == "<symbol>" and tkn[1] == "]" and tkn[2] =="</symbol>"):
                print_indent()
                parsed_lines.append(tokens[curr_idx])
            else:
                raise Exception("Unexpected token "+tkns+" seen; symbol ] expected in term")
        if (tkn_plus[0] == "<symbol>" and tkn_plus[1] in ['(','.'] and tkn_plus[2] =="</symbol>"):
            curr_idx = curr_idx + 1
            tkns = tokens[curr_idx]
            tkn = tkns.split()
            if (tkn[0] == "<symbol>" and tkn[1] == '(' and tkn[2] =="</symbol>"):
                print_indent()
                parsed_lines.append(tokens[curr_idx])
                
                compile_expressionList()
                
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in term")
            if (tkn[0] == "<symbol>" and tkn[1] == '.' and tkn[2] =="</symbol>"):
                print_indent()
                parsed_lines.append(tokens[curr_idx])
                
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Unexpected token "+tkns+" seen; identifier expected in term")
                
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<symbol>" and tkn[1] == "(" and tkn[2] =="</symbol>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Unexpected token "+tkns+" seen; symbol ( expected in term")
                
                compile_expressionList()
                    
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in term")
                
    elif (tkn[0] == "<symbol>" and tkn[1] == "(" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        compile_expression()
        
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in term")
    elif (tkn[0] == "<symbol>" and (tkn[1] == '-' or tkn[1] == '~') and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        compile_term()
       
    else:
        raise Exception("Unexpected token "+tkns+" seen; expect a valid symbol - or ~ instead")
    
    indent_minus()
    print_indent()
    parsed_lines.append("</term>\n")

def compile_expression():
    global curr_idx
    print_indent()
    parsed_lines.append("<expression>\n")
    indent_plus()

    tkns = tokens[curr_idx]
    tkn = tkns.split()
    compile_term()
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    while (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] in ['+','-','*','/','&amp;','|','&lt;','&gt;','=']):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        compile_term()
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
    
    indent_minus()
    print_indent()
    parsed_lines.append("</expression>\n")



def compile_whileStatement():
    global curr_idx
    print_indent()
    parsed_lines.append("<whileStatement>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    print_indent()
    parsed_lines.append(tokens[curr_idx])
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == '(' and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ( expected in whileStatement")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    compile_expression()

    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in whileStatement")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == "{"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol { expected in whileStatement")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    print_indent()
    parsed_lines.append("<statements>\n")
    indent_plus()
    while ((tkn[0] != "<symbol>") and (tkn[1] != "}") and (tkn[2] != "</symbol>")):
        compile_statement()
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
    
    indent_minus()
    print_indent()
    parsed_lines.append("</statements>\n")
    if (tkn[0] == "<symbol>" and tkn[1] == "}" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol } expected in whileStatement")
        
    indent_minus()
    print_indent()
    parsed_lines.append("</whileStatement>\n")

def compile_ifStatement():
    global curr_idx
    print_indent()
    parsed_lines.append("<ifStatement>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    print_indent()
    parsed_lines.append(tokens[curr_idx])
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == '(' and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ( expected in ifStatement")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    compile_expression()

    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in ifStatement")
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == "{"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol { expected in ifStatement")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    print_indent()
    parsed_lines.append("<statements>\n")
    indent_plus()
    while ((tkn[0] != "<symbol>") and (tkn[1] != "}") and (tkn[2] != "</symbol>")):
        compile_statement()
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
    
    indent_minus()
    print_indent()
    parsed_lines.append("</statements>\n")
    if (tkn[0] == "<symbol>" and tkn[1] == "}" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol } expected in ifStatement")
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[1] == "else" and tkn[2] =="</keyword>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])

        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == "{"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol { expected in ifStatement")
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        print_indent()
        parsed_lines.append("<statements>\n")
        indent_plus()
        while ((tkn[0] != "<symbol>") and (tkn[1] != "}") and (tkn[2] != "</symbol>")):
            compile_statement()
        
            curr_idx = curr_idx + 1
            tkns = tokens[curr_idx]
            tkn = tkns.split()
    
        indent_minus()
        print_indent()
        parsed_lines.append("</statements>\n")
        if (tkn[0] == "<symbol>" and tkn[1] == "}" and tkn[2] =="</symbol>"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol } expected in ifStatement")
    else:
        curr_idx = curr_idx - 1
            
    indent_minus()
    print_indent()
    parsed_lines.append("</ifStatement>\n")
            
    
def compile_returnStatement():
    global curr_idx
    print_indent()
    parsed_lines.append("<returnStatement>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    print_indent()
    parsed_lines.append(tokens[curr_idx])
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == ';' and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        compile_expression()
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<symbol>" and tkn[1] == ';' and tkn[2] =="</symbol>"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol ; expected in returnStatement")
    
    indent_minus()
    print_indent()
    parsed_lines.append("</returnStatement>\n")


def compile_doStatement():
    global curr_idx
    print_indent()
    parsed_lines.append("<doStatement>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    print_indent()
    parsed_lines.append(tokens[curr_idx])
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        tkns_plus = tokens[curr_idx+1]
        tkn_plus = tkns_plus.split()

        if (tkn_plus[0] == "<symbol>" and tkn_plus[1] in ['(','.'] and tkn_plus[2] =="</symbol>"):
            curr_idx = curr_idx + 1
            tkns = tokens[curr_idx]
            tkn = tkns.split()
            if (tkn_plus[0] == "<symbol>" and tkn_plus[1] == '(' and tkn_plus[2] =="</symbol>"):
                print_indent()
                parsed_lines.append(tokens[curr_idx])
                
                compile_expressionList()
                
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in doStatement")
            if (tkn_plus[0] == "<symbol>" and tkn_plus[1] == '.' and tkn_plus[2] =="</symbol>"):
                print_indent()
                parsed_lines.append(tokens[curr_idx])
                
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Invalid term seen")
                
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<symbol>" and tkn[1] == "(" and tkn[2] =="</symbol>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Unexpected token "+tkns+" seen; symbol ( expected in doStatement")
                    
                compile_expressionList()
                    
                curr_idx = curr_idx + 1
                tkns = tokens[curr_idx]
                tkn = tkns.split()
                if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
                    print_indent()
                    parsed_lines.append(tokens[curr_idx])
                else:
                    raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in doStatement")
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == ";" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        indent_minus()
        print_indent()
        parsed_lines.append("</doStatement>\n")
    else:
        raise Exception("expects symbol ;")


def compile_letStatement():
    global curr_idx
    print_indent()
    parsed_lines.append("<letStatement>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    print_indent()
    parsed_lines.append(tokens[curr_idx])
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; identifier expected in letStatement")

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == "[" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        compile_expression()

        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<symbol>" and tkn[1] == "]" and tkn[2] =="</symbol>"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol ] expected in letStatement")
            
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        
    if (tkn[0] == "<symbol>" and tkn[1] == "=" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol = expected in letStatement")
    
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    compile_expression()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == ";" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        indent_minus()
        print_indent()
        parsed_lines.append("</letStatement>\n")
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ; expected in letStatement")

def compile_statement():
    global curr_idx
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>"):
        if (tkn[1] == "let"):
            compile_letStatement()
        if (tkn[1] == "if"):
            compile_ifStatement()
        if (tkn[1] == "while"):
            compile_whileStatement()
        if (tkn[1] == "do"):
            compile_doStatement()
        if (tkn[1] == "return"):
            compile_returnStatement()



def compile_varDec():
    global curr_idx
    print_indent()
    parsed_lines.append("<varDec>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>" and tkn[1] == "var"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; keyword expected in varDec")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>"):
        if (tkn[1] == "int" or tkn[1] == "char" or tkn[1] == "boolean"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; int, char or boolean keyword expected in varDec")
    elif (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; identifier expected in varDec")

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    while ((tkn[0] != "<symbol>") or (tkn[1] != ";") or (tkn[2] != "</symbol>")):
        if ((tkn[0] == "<symbol>") and (tkn[1] == ",") and (tkn[2] == "</symbol>")):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol , expected in varDec")
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol , expected in varDec")
            
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        
    if ((tkn[0] == "<symbol>") and (tkn[1] == ";") and (tkn[2] == "</symbol>")):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ; expected in varDec")

    indent_minus()
    print_indent()
    parsed_lines.append("</varDec>\n")



def compile_subroutineBody():
    global curr_idx
    print_indent()
    parsed_lines.append("<subroutineBody>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[2] =="</symbol>" and tkn[1] == "{"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol { expected in subroutineBody")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    
    while ((tkn[0] == "<keyword>") and tkn[1] == "var" and tkn[2] == "</keyword>"):
        compile_varDec()
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
    
    print_indent()
    parsed_lines.append("<statements>\n")
    indent_plus()
    while ((tkn[0] != "<symbol>") and (tkn[1] != "}") and (tkn[2] != "</symbol>")):
        compile_statement()
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()

    indent_minus()
    print_indent()
    parsed_lines.append("</statements>\n")
    if (tkn[0] == "<symbol>" and tkn[1] == "}" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol } expected in subroutineBody")
        
    indent_minus()
    print_indent()
    parsed_lines.append("</subroutineBody>\n")



def compile_subroutineDec():
    global curr_idx
    print_indent()
    parsed_lines.append("<subroutineDec>\n")
    indent_plus()
    
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>" and ((tkn[1] == "function") or (tkn[1] == "method") or (tkn[1] == "constructor"))):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; constructor or function or method keyword expected in subroutineDec")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>"):
        if (tkn[1] == "int" or tkn[1] == "char" or tkn[1] == "boolean" or tkn[1] == "void"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; int, char or boolean keyword expected in subroutineDec")
    elif (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; identifier expected in subroutineDec")
        
            
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; identifier expected in subroutineDec")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == "(" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ( expected in subroutineDec")
        
    compile_parameterList()
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == ")" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ) expected in subroutineDec")

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    compile_subroutineBody()

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>" and ((tkn[1] == "function") or (tkn[1] == "method") or (tkn[1] == "constructor"))):
        indent_minus()
        print_indent()
        parsed_lines.append("</subroutineDec>\n")
        compile_subroutineDec()
    else:
        indent_minus()
        print_indent()
        parsed_lines.append("</subroutineDec>\n")
        curr_idx = curr_idx - 1



def compile_classVarDec():
    global curr_idx
    print_indent()
    parsed_lines.append("<classVarDec>\n")
    indent_plus()

    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>" and ((tkn[1] == "static") or (tkn[1] == "field"))):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; keyword static or field expected in classVarDec")
                
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>"):
        if (tkn[1] == "int" or tkn[1] == "char" or tkn[1] == "boolean"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; keyword int, char or boolean expected in classVarDec")
    elif (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; identifier expected in classVarDec")

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; identifier expected in classVarDec")
            
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    while ((tkn[0] != "<symbol>") or (tkn[1] != ";") or (tkn[2] != "</symbol>")):      
        if ((tkn[0] == "<symbol>") and (tkn[1] == ",") and (tkn[2] == "</symbol>")):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; symbol , expected in classVarDec")
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if (tkn[0] == "<identifier>" and tkn[2] =="</identifier>"):
            print_indent()
            parsed_lines.append(tokens[curr_idx])
        else:
            raise Exception("Unexpected token "+tkns+" seen; identifier expected in classVarDec")
            
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()

    if ((tkn[0] == "<symbol>") and (tkn[1] == ";") and (tkn[2] == "</symbol>")):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; symbol ; expected in classVarDec")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<keyword>" and tkn[2] =="</keyword>" and ((tkn[1] == "static") or (tkn[1] == "field"))):
        indent_minus()
        print_indent()
        parsed_lines.append("</classVarDec>\n")
        compile_classVarDec()
    else:
        indent_minus()
        print_indent()
        parsed_lines.append("</classVarDec>\n")
        curr_idx = curr_idx - 1



#program structure compilations
def compile_class():
    global curr_idx
    parsed_lines.append("<class>\n")
    indent_plus()
    print_indent()
    parsed_lines.append("<keyword> class </keyword>\n")

    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] != "<identifier>" and tkn[2] !="</identifier>"):
        raise Exception("Unexpected token "+tkns+" seen; class expects className identifier")
    else:
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    if (tkn[0] == "<symbol>" and tkn[1] == "{" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
    else:
        raise Exception("Unexpected token "+tkns+" seen; class expects { symbol")
        
    curr_idx = curr_idx + 1
    tkns = tokens[curr_idx]
    tkn = tkns.split()
    while ((tkn[0] != "<symbol>") or (tkn[1] != "}") or (tkn[2] != "</symbol>")):
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if ((tkn[1] == "static") or (tkn[1] == "field")):
            compile_classVarDec()  

        tkns = tokens[curr_idx]
        tkn = tkns.split()
        if ((tkn[1] == "constructor") or (tkn[1] == "function") or (tkn[1] == "method")):
            compile_subroutineDec()
        
        curr_idx = curr_idx + 1
        tkns = tokens[curr_idx]
        tkn = tkns.split()
        
    if (tkn[0] == "<symbol>" and tkn[1] == "}" and tkn[2] =="</symbol>"):
        print_indent()
        parsed_lines.append(tokens[curr_idx])
        indent_minus()
        print_indent()
        parsed_lines.append("</class>\n")
    else:
        raise Exception("Unexpected token "+tkns+" seen; class expects } symbol")



if (tokens[0] == "<tokens>\n" and tokens[1] == "<keyword> class </keyword>\n"):
    compile_class()



xml_file_name = filename.replace(".jack",".xml")
open(xml_file_name, 'w').close()
file_xml = open(xml_file_name,"a")
for pl in parsed_lines:
    file_xml.write(pl)
file_xml.close()


jack_file.close()
