TITLE Project 6 (The Last One)     (Proj6_backujed.asm)

; Author: Jedidiah Backus
; Last Modified:  8/18/2023
; OSU email address: backujed@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: Project 6   Due Date:  8/18/2023
; Description:	Program takes 10 numbers as strings, checking to ensure the inputs are indeed numbers, converts them to integers and stores them in an array. 
;					Program then converts them back to strings, prints the strings showing what was input, and then calculates and displays the total sum and the average of the numbers


INCLUDE Irvine32.inc

; ---------------------------------------------------------------------------------
; Name: mGetString
;
; Prompts user to input a string, and then accepts the string
;
; Preconditions: none.
;
; Receives:	prompt:		String to be displayed as prompt for user
;			dest:		Desired destination for string
;			maxSize:	Max number of characters to be accepted
;			num_chars:	The number of characters entered (output)
;
; returns: String for program to convert to number
; ---------------------------------------------------------------------------------

mGetString	MACRO	prompt:REQ, dest:REQ, maxSize:REQ, num_chars:REQ
	PUSH	EAX
	PUSH	EDX
	PUSH	ECX
	MOV		EDX, prompt
	Call	WriteString
	MOV		ECX, maxSize
	MOV		EDX, dest
	Call	ReadString
	MOV		num_chars, EAX
	POP		ECX
	POP		EDX
	POP		EAX
ENDM





; ---------------------------------------------------------------------------------
; Name: mDisplayString
;
; Displays a string passed to the Macro
;
; Preconditions: none.
;
; Receives:	target:		String to be displayed
; 
;
; returns: none.
; ---------------------------------------------------------------------------------

mDisplayString MACRO target:REQ
	PUSH	EAX
	MOV		EAX, target
	Call	WriteChar
	POP		EAX
ENDM




MAX_CHAR	=	32
ARRAYSIZE	=	10

.data

intro		BYTE	"Welcome to my program 'Project 6'. This program demonstrates the use of String Primatives and Macros.", 13, 10, 13, 10, 0
explain1	BYTE	"To use this program you will need to enter 10 signed integers. Any input other than a digit, a '+' or '-' sign, ", 13, 10, 0
explain2	BYTE	"or if the input is too large for a 32-bit register, will be rejected and a new valid number will be requested.", 13, 10, 13, 10, 0
explain3	BYTE	"Once 10 valid numbers have been entered, this program will calculate and display the numbers, the sum of the numbers, and the average value of the numbers. Enjoy.", 13, 10, 13, 10, 0
input		BYTE	320 DUP(?)
total_char	DWORD	?
bad_num		DWORD	0
numArray	SDWORD	ARRAYSIZE DUP(?)
inPrompt	BYTE	"Please enter a valid integer: ", 0
badInput	BYTE	"The number you entered was not valid.", 0
testing		BYTE	"this is just a test", 0
out_prompt	BYTE	"The valid numbers you entered are: ", 13, 10, 0
total		SDWORD	?
average		SDWORD	?
sumPrompt	BYTE	"The sum of all your numbers is: ", 0
avPrompt	BYTE	"The truncated average is: ", 0
outstring	BYTE	32 DUP(?)




.code
main PROC

	PUSH	OFFSET	intro											; Sets up and calls the intro, including telling the user how the program should work
	PUSH	OFFSET	explain1
	PUSH	OFFSET	explain2
	PUSH	OFFSET	explain3
	CALL	introduction	
	MOV		ECX, ARRAYSIZE											; Sets ECX to the length of the array to be filled (default is 10)
	MOV		EDI, OFFSET numArray
_get_numbers:
	PUSH	ECX
	PUSH	OFFSET inPrompt
	PUSH	OFFSET input
	PUSH	OFFSET badInput
	PUSH	total_char
	PUSH	OFFSET numArray
	PUSH	OFFSET bad_num
	CALL	ReadVal													; Calls the ReadVal procedure to get a string and convert it to a number
	CMP		bad_num, 1												; If the user entered anything other than a valid number, the ReadVal procedure will have set bad_num to 1
	JE		_bad_num
	MOV		EDX, [ESP-60]											; If it's a good number, it'll be saved in the array
	MOV		[EDI], EDX
	ADD		EDI, 4
	POP		ECX
	MOV		bad_num, 0
	LOOP	_get_numbers
	JMP		_done_getting_nums

_bad_num:															; If bad_num has been set to one, saving the number is skipped and ECX is incremented so the right number of numbers is still recieved
	POP		ECX
	INC		ECX
	MOV		bad_num, 0
	LOOP	_get_numbers

_done_getting_nums:													; Once the array is filled, this section will print out the numbers as strings by calling the WriteVal procedure
	Call	CrLf
	Call	CrLf
	MOV		EDX, OFFSET out_prompt									; Prompt to tell the user that their numbers are being printed back
	Call	WriteString
	MOV		ECX, LENGTHOF numArray
	MOV		EDX, OFFSET numArray
_print_numbers:														; Loops through array, calling WriteVal which converts and prints numbers as strings
	PUSH	EDX
	PUSH	OFFSET outstring
	CALL	WriteVal
	ADD		EDX, 4
	MOV		AL, 44													; Adds a comma after a printed number (need to remove last comma if time allows)
	Call	WriteChar
	MOV		AL,	32													; Adds a space after a printed number
	Call	WriteChar
	LOOP	_print_numbers
	XOR		EBX, EBX
	MOV		EDX, OFFSET numArray
	MOV		ECX, LENGTHOF numArray
_add_nums:															; This section adds all the numbers in the array together and prints the total using the WriteVal procedure
	MOV		EAX, [EDX]
	ADD		EBX, EAX
	ADD		EDX, 4
	LOOP	_add_nums
	Call	CrLf
	Call	CrLf
	MOV		EDX, OFFSET sumPrompt
	Call	WriteString
	MOV		total, EBX
	PUSH	OFFSET total
	PUSH	OFFSET outstring
	Call	WriteVal
	Call	CrLf
	Call	CrLf
	XOR		EAX, EAX												; This section finds the average of the numbers and prints it using the WriteVal procedure
	XOR		EDX, EDX
	MOV		EAX, total
	MOV		EBX, ARRAYSIZE
	IDIV	EBX
	MOV		average, EAX
	MOV		EDX, OFFSET avPrompt
	Call	WriteString
	PUSH	OFFSET average
	PUSH	OFFSET outstring
	CALL	WriteVal
	Call	CrLf

  exit
main ENDP


	Invoke ExitProcess,0	; exit to operating system


; ---------------------------------------------------------------------------------
; Name: introduction
;
; Introduces the program and programmer to the user. 
;
; Preconditions: none. 
;
; Postconditions: none.
;
; Receives: [ESP+24]	=	address of intro (string)
;			[ESP+20]	=	address of explain1 (string)
;			[ESP+16]	=	address of explain2 (string)
;			[ESP+12]	=	address of explain3 (string)
;
; returns: none.
; ---------------------------------------------------------------------------------

introduction PROC USES EDX

	PUSH	EBP
	MOV		EDX, [ESP+24]						; address of intro
	Call	WriteString
	MOV		EDX, [ESP+20]						; address of explain1
	Call	WriteString
	MOV		EDX, [ESP+16]						; address of explain2
	Call	WriteString
	MOV		EDX, [ESP+12]						; address of explain3
	Call	WriteString
	POP		EBP
	RET		16

introduction ENDP





; ---------------------------------------------------------------------------------
; Name: ReadVal
;
; Takes an input from the user and checks that it is valid, if valid stores the input.
;		if not valid, rejects input and prompts for another input.
;
; Preconditions: All the needed data has been pushed to the stack 
;
; Postconditions: none.
;
; Receives: [EBP+52]	=	String prompt for getting a variable
;			[EBP+28]	=	Destination for numbers
;			[EBP+40]	=	Where to store character count to be used in counter
;			[EBP+44]	=	String prompt to let the user know they input an invalid character
;			[EBP+32]	=	Destination for invalid character indicator
;
; returns: A valid string converted to a number, or alters an indicator to show input was invalid.
; ---------------------------------------------------------------------------------

ReadVal PROC USES EAX EBX ECX EDX EDI ESI

	PUSH	EBP
	MOV		EBP, ESP
	CLD
	mGetString	[EBP+52], [EBP+48], MAX_CHAR, [EBP+40]				; Gets the string from the user
	MOV		ECX, [EBP+40]											; Sets the counter to the number of characters the user entered
	MOV		ESI, [EBP+48]
	XOR		EAX, EAX
	XOR		EDX, EDX
	XOR		EBX, EBX
_check_valid:														; Checks if the user entered a valid number
	LODSB															; Loads the first ASCII decimal value representing the first character
	CMP		AL, 45													; Checks if the first character is a negative sign, if so jumps to neg number section
	JE		_its_a_neg
	CMP		AL, 43													; Checks if the character is a positive sign, if so skips to the next character
	JE		_pos_num
	CMP		AL, 48													; Checks that the character equals out to between 0 and 9, otherwise it's invalid
	JB		_invalid_number
	CMP		AL, 57
	JA		_invalid_number
	SUB		AL, 48													; Converts string to number
	PUSH	EAX
	MOV		EAX, EDX
	MOV		EBX, 10
	IMUL	EBX														
	JO		_invalid_number											; Checks overflow flag, if set number is too large and rejected
	MOV		EDX, EAX
	POP		EAX
	MOVZX	EBX, AL
	ADD		EDX, EBX
	JO		_invalid_number											; Checks overflow flag, if set number is too large and rejected
	LOOP	_check_valid
_back_from_neg:
	PUSH	EDX
	POP		EDX

_finish:
	STD
	POP		EBP
	RET		24

_pos_num:
	LOOP	_check_valid											; If the first character was a positive sign, this will loop back bringing up the next character

_its_a_neg:
	DEC		ECX														; This section is mostly the same as above, but has some specifics for negative numbers
_still_a_neg:														; Decrementing the counter keeps it from adding the negative sign into the math
	LODSB
	CMP		AL, 48
	JB		_invalid_number
	CMP		AL, 57
	JA		_invalid_number
	SUB		AL, 48
	PUSH	EAX
	MOV		EAX, EDX
	MOV		EBX, 10
	IMUL	EBX
	JO		_invalid_number
	MOV		EDX, EAX
	POP		EAX
	MOVZX	EBX, AL
	ADD		EDX, EBX
	JO		_invalid_number
	DEC		ECX
	CMP		ECX, 0
	JNZ		_still_a_neg
	IMUL	EDX, -1													; Multiplying the converted number by -1 turns it negative (main difference from how positives are handled)
	LOOP	_back_from_neg

_invalid_number:
	MOV		EDX, [EBP+44]											; Prompt letting user know they entered an invalid number (either not a number or too large)
	Call	WriteString
	Call	CrLf
	MOV		EDI, [ESP+32]
	MOV		EAX, 1
	MOV		[EDI], EAX												; Sets the bad number indicator so the program won't save it and asks for a new number
	JMP		_finish

ReadVal ENDP





; ---------------------------------------------------------------------------------
; Name: ReadVal
;
; Takes a number, converts it to a string and then prints it to the console
;		
;
; Preconditions: number to be converted and displayed is pushed to the stack
;
; Postconditions: none.
;
; Receives: [EBP+32]	=	Destination for converted characters
;			[EBP+36]	=	number to be converted and displayed
;
; returns: Displays a number as a string
; ---------------------------------------------------------------------------------

WriteVal PROC USES EAX EBX ECX EDX EDI ESI

	PUSH	EBP
	MOV		EBP, ESP

	MOV		EDI, [EBP+32]
	MOV		EDX, [EBP+36]
	MOV		EAX, [EDX]
	XOR		EDX, EDX
	MOV		EBX, 10
	IDIV	EBX
	ADD		EDX, 48
	MOV		EAX, EDX
	mDisplayString	EAX



	;	Incomplete. My plan was to take the number and divide by 10, adding 48 to the remainder to result in the ASCII decimal value, and then looping through until there was nothign left
	;		I struggled with getting the character count for numbers that were multiple digits, and then with how to either store them backwards or display them backwards so they were
	;		 n the right order. I assume this is done with the direction flag, but in all my playing with it I couldn't make it work. I'll keep working on it for my own satisfaction. 
			




	POP		EBP
	RET		8

WriteVal ENDP


END main