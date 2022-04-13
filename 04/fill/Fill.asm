// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP1)
	@KBD
	D=M
	@UNPRESSED
	D;JEQ
	@PRESSED
	D;JNE

	(PRESSED)
		@SCREEN
		D=A
		(LOOP_BLACK)
			A=D
			M=-1
			D=A+1
			@0
			M=D    //current D
			@1
			M=D    //copy of current D
			@KBD
			D=A
			@0
			M=D-M    //check if D is same as KBD
			@LOOP1
			M;JEQ
			@1
			D=M  //restore D from copy of current D
			@LOOP_BLACK
			0;JMP
			
	(UNPRESSED)
		@SCREEN
		D=A
		(LOOP_WHITE)
			A=D
			M=0
			D=A+1
			@0
			M=D    //current D
			@1
			M=D    //copy of current D
			@KBD
			D=A
			@0
			M=D-M       //check if D is same as KBD
			@LOOP1
			M;JEQ
			@1
			D=M  //restore D from copy of current D
			@LOOP_WHITE
			0;JMP
	
@LOOP1
0;JMP