# Chronos
## By Zasharan2
Chronos is a befunge-based esoteric programming language whose main feature is the ability to travel through time. Through the use of the "t" instruction, cursors within a program may time travel, creating a branch universe that has its own cursor.<br /><br />
**Run**<br />
    To run a program, run the python file chronos.py, followed with --file FILENAME, where FILENAME is the file you wish to run.<br />
    All chronos files should have a .time extension.<br />
    If you wish to view the program space as the program runs, you may use the --debug toggle to turn on debug mode.<br />
    If you wish to "step" through each moment, you may use the --step toggle to turn on step mode, and press enter each time you wish to "step".<br />
<br />
**Syntax**<br />
    > = set cursor orientation right<br />
    < = set cursor orientation left<br />
    ^ = set cursor orientation up<br />
    v = set cursor orientation down<br />
    + = pop a, b, push a+b<br />
    - = pop a, b, push b-a<br />
    * = pop a, b, push a*b<br />
    / = pop a, b, push b/a<br />
    % = pop a, b, push b%a<br />
    0-9 = push number<br />
    ? = pop a, skip next if not zero<br />
    ! = pop a, if not 0, push 0, otherwise push 1<br />
    g = pop y, x, push char in prog at (x,y)<br />
    p = pop y, x, v, write v to prog at (x,y)<br />
    : = duplicate top stack elem<br />
    \ = swap top two stack elems<br />
    " = toggle stringmode<br />
    , = pop a, output<br />
    i = push input char<br />
    t = pop a, time travel to time t=a<br />
    @ = end program<br />
<br />
**Time travel**<br />
    Cursors will move around.<br />
    Each completion of an instruction is one moment of time (t++).<br />
    Upon completing a time travel instruction, the cursor will travel to time t=a, then finish its move.<br />
    The next completion of the recently time-travelled cursor will be at time t=a+1.<br />
    It will not complete an instruction at time t=a.<br />
    This form of time travel will follow a branching universe framework, though this will not be displayed to the programmer.<br />
    The only printed results will be those of the final branch.<br />
<br />
**Stacks**<br />
    Each cursor will have one local stack.<br />
    If there are multiple cursors in one moment, each cursor will only be able to access its own local stack.<br />
<br />
**Cursor intersection**<br />
    If two cursors end up at the same location in one moment, and if their respective completions of their instructions interfere with one another, then the cursor that has time travelled from the latest branching point will take priority.
<br />
