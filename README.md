Run:
To run a program, run the python file chronos.py, followed with --file FILENAME, where FILENAME is the file you wish to run.
All chronos files should have a .time extension.
If you wish to view the program space as the program runs, you may use the --debug toggle to turn on debug mode.
If you wish to "step" through each moment, you may use the --step toggle to turn on step mode, and press enter each time you wish to "step".

Syntax:
    > = set cursor orientation right
    < = set cursor orientation left
    ^ = set cursor orientation up
    v = set cursor orientation down
    + = pop a, b, push a+b
    - = pop a, b, push b-a
    * = pop a, b, push a*b
    / = pop a, b, push b/a
    % = pop a, b, push b%a
    0-9 = push number
    ? = pop a, skip next if not zero
    ! = pop a, if not 0, push 0, otherwise push 1
    g = pop y, x, push char in prog at (x,y)
    p = pop y, x, v, write v to prog at (x,y)
    : = duplicate top stack elem
    \ = swap top two stack elems
    " = toggle stringmode
    , = pop a, output
    i = push input char
    t = pop a, time travel to time t=a
    @ = end program

Time travel:
    Cursors will move around.
    Each completion of an instruction is one moment of time (t++).
    Upon completing a time travel instruction, the cursor will travel to time t=a, then finish its move.
    The next completion of the recently time-travelled cursor will be at time t=a+1.
    It will not complete an instruction at time t=a.
    This form of time travel will follow a branching universe framework, though this will not be displayed to the programmer.
    The only printed results will be those of the final branch.

Stacks:
    Each cursor will have one local stack.
    If there are multiple cursors in one moment, each cursor will only be able to access its own local stack.

Cursor intersection:
    If two cursors end up at the same location in one moment, and if their respective completions of their instructions interfere with one another, then the cursor that has time travelled from the latest branching point will take priority.
