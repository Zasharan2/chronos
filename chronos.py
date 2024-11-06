import argparse
import copy
import sys

# Arguments (file, debug)
parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", help = "File input (str)", type=str)
parser.add_argument("--debug", "-d", help = "Debug mode (boolean)", action="store_true")
parser.add_argument("--step", "-s", help = "Step mode (boolean)", action="store_true")

args = parser.parse_args()
if (vars(args)["file"].find(".time")) and (vars(args)["file"][-5:] == ".time"):
    file = open(vars(args)["file"], 'r')
else:
    raise ValueError("Unrecognized file extension (should be .time).")

debug_mode = vars(args)["debug"]
step_mode = vars(args)["step"]

# Obtain program and inputs
original_program = file.read().split("\n")

sys.stdout.write("Input(s): ")
original_inputs = input()
inputs = copy.copy(original_inputs)

# Vector2
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

# Cursor
class Cursor:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.dir = Vector2(1, 0)
        self.stack = []

        self.stringMode = False
        self.timeTravel = False
        self.end = False
    
    def compute(self, program):
        global printList
        value = program[self.pos.y][self.pos.x]
        if self.stringMode:
            if value == "\"":
                self.stringMode = False
            else:
                self.stack.append(ord(value))
        else:
            if value == ">":
                self.dir = Vector2(1, 0)
            elif value == "<":
                self.dir = Vector2(-1, 0)
            elif value == "^":
                self.dir = Vector2(0, -1)
            elif value == "v":
                self.dir = Vector2(0, 1)
            elif value.isdigit():
                self.stack.append(int(value))
            elif value == "+":
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a + b)
            elif value == "-":
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b - a)
            elif value == "*":
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a * b)
            elif value == "/":
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b // a)
            elif value == "%":
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b % a)
            elif value == "?":
                # Extra move if popped value not 0
                a = self.stack.pop()
                if (not type(a) == int) or (type(a) == int and (not a == 0)):
                    self.move()
            elif value == "!":
                # Set all nonzero to 0, and 0 to 1
                a = self.stack.pop()
                if (not type(a) == int) or (type(a) == int and (not a == 0)):
                    self.stack.append(0)
                else:
                    self.stack.append(1)
            elif value == "g":
                y = self.stack.pop()
                x = self.stack.pop()
                self.stack.append(ord(program[y][x]))
            elif value == "p":
                y = self.stack.pop()
                x = self.stack.pop()
                v = self.stack.pop()
                program[y] = program[y][:x] + chr(v) + program[y][x + 1:]
            elif value == ":":
                self.stack.append(self.stack[len(self.stack) - 1])
            elif value == "\\":
                a = self.stack[len(self.stack) - 1]
                self.stack[len(self.stack) - 1] = self.stack[len(self.stack) - 2]
                self.stack[len(self.stack) - 2] = a
            elif value == ".":
                a = self.stack.pop()
                printList.append(str(a))
            elif value == ",":
                a = self.stack.pop()
                printList.append(chr(a))
            elif value == "\"":
                self.stringMode = True
            elif value == "i":
                global inputs
                if len(inputs[-1:]) > 0:
                    self.stack.append(ord(inputs[-1:]))
                    inputs = inputs[:-1]
                else:
                    self.stack.append(-1)
            elif value == "t":
                a = self.stack.pop()
                self.timeTravel = a
                self.end = True
            elif value == "@":
                self.end = True

        self.move()
    
    def print(self, program):
        program[self.pos.y] = program[self.pos.y][:self.pos.x] + "█" + program[self.pos.y][self.pos.x + 1:]
        for string in program:
            print(string)
        print("")
        print("Stack: " + str(self.stack))
        print("--------------")
        print("")
    
    def move(self):
        self.pos += self.dir

printList = []
cursorList = []

def run(program):
    global cursorList
    global original_inputs
    global inputs

    inputs = original_inputs

    allCursorEnd = False
    timeTravelEvent = False
    time = 0
    while (not allCursorEnd):
        allCursorEnd = True

        # Printing
        if (debug_mode):
            printProg = copy.copy(program)
            for cursor in cursorList:
                if cursor.timeTravel == False and cursor.end == False:
                    printProg[cursor.pos.y] = printProg[cursor.pos.y][:cursor.pos.x] + "█" + printProg[cursor.pos.y][cursor.pos.x + 1:]
                elif type(cursor.timeTravel) != bool and cursor.timeTravel == time and cursor.end == False:
                    printProg[cursor.pos.y] = printProg[cursor.pos.y][:cursor.pos.x] + "█" + printProg[cursor.pos.y][cursor.pos.x + 1:]
            for string in printProg:
                print(string)
            print("")
            print("--------------")
            print("")

        for cursor in cursorList:
            # The cursor has time travelled from another timeline
            if type(cursor.timeTravel) != bool and cursor.end == False:
                # Once the program has reached the proper time, "place" the cursor there by setting its time travel to false
                if cursor.timeTravel == time:
                    cursor.timeTravel = False
            # Run cursor logic
            if cursor.timeTravel == False and cursor.end == False:
                cursor.compute(program)
            # Check cursor end
            if cursor.end == False:
                allCursorEnd = False
            # Check time travel
            if type(cursor.timeTravel) != bool and cursor.end == True:
                timeTravelEvent = True
        # Wait for user to "step" manually
        if step_mode:
            input()
        time += 1
    if timeTravelEvent:
        if (debug_mode):
            print("============================")
            print("NEW TIMELINE")
            print("============================")
            print("")
        for cursor in cursorList:
            # Eliminate all non-timetravellers, set the timetravllers end to false
            if type(cursor.timeTravel) != bool:
                cursor.end = False
            else:
                cursorList.pop(cursorList.index(cursor))
        # Create new cursor for new timeline
        newCursor = [Cursor()]
        newCursor.extend(cursorList)
        cursorList = newCursor
        global printList
        printList = []
        # Run with new cursors
        run(copy.copy(original_program))

# Run with one cursor
cursorList = [Cursor()]
run(copy.copy(original_program))

# Print final printList
print("".join(printList))