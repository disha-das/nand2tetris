@111
D=A
@SP
A=M
M=D
@SP
M=M+1

@333
D=A
@SP
A=M
M=D
@SP
M=M+1

@888
D=A
@SP
A=M
M=D
@SP
M=M+1

@StaticTest.vmstatic8
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@StaticTest.vmstatic3
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@StaticTest.vmstatic1
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@StaticTest.vmstatic3
D=M
@SP
A=M
M=D
@SP
M=M+1

@StaticTest.vmstatic1
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
A=M
A=A-1
D=M
A=A-1
M=M-D
@SP
M=M-1

@StaticTest.vmstatic8
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
A=M
A=A-1
D=M
A=A-1
M=D+M
@SP
M=M-1

