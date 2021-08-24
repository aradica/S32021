# S32021
Register based virtual machine (vm) implemented in Python 3.

# Usage
    python fhvm.py <filename>

## Optional arguments
To specify the amount of virtual memory, use
    --registers N

Maximum program size
    --maxprogram N
    
# Opcodes
X - value

P - program

R - register

## I/O
Load integer X into register R

    LOAD X R

Prints the value stored in R

    PRINT R
    
Load integer X into register pointed by R

    LOADP X R

Prints the value stored in register pointed by R

    PRINTP R

Inputs integer into R

    INPUT R

Inputs integer to register pointed by R

    INPUTP R

Copies the value from R1 to R2

    COPY R1 R2


## Arithmetic

Increments R by 1

    INC R

Stores R1+R2 into R3

    ADD R1 R2 R3

Stores R1-R2 into R3

    SUB R1 R2 R3

Stores R1*R2 into R3

    MUL R1 R2 R3

Stores R1//R2 into R3

    DIV R1 R2 R3

## Jumps
Sets program pointer to P if R1 > R2

    GOG P R1 R2

Sets program pointer to P if R1 < R2

    GOL P R1 R2
    
Sets program pointer to P if R1 = R2

    GOE P R1 R2
 
Sets program pointer to P

    GOTO P

# Halt & other

Halts the program

    HALT

Modifies the program instruction to X

    META P X

Does nothing

    NOP
