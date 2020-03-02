import __init__ as ps
import sys

try:
    color = sys.stdout.shell
except:
    raise RuntimeError("Use IDLE")

def dbgmain(inputs):
    pictures = {}
    original_pictures = {}
    undo = {}
    for inp in inputs:
        color.write(inp, "TEXT")
        print()
        param = ps.get_parameters(inp)
        if not param:
            continue
        command = param[0]
        if command == "exit":
            return True
        ps.process_command(command, param, pictures, original_pictures, undo)

file = open("tests.txt", 'r')
commands = file.readlines()
inputs = list()
for i in range(len(commands)):
    if commands[i][0] == '#':
        continue
    if commands[i][-1] == '\n':
        inputs.append(commands[i][:-1])
        com = commands[i].split()
        nxtcmd = "save p tests\\" + com[0] + '\\'
        if len(com) >= 3:
            nxtcmd += com[2]
        if len(com) >= 4:
            nxtcmd += '_' + com[3]
        nxtcmd += ".jpg"
        inputs.append(nxtcmd)
        if com[0] == "modify" or com[0] == "effect":
            inputs.append("reset p")
    #commands[i] = commands[i].split()
dbgmain(inputs)

    
##issues = []
##for command in commands:
##    out = ps.process_commands(' '.join(command), file=sys.stderr)
##    out = ' '.join(command)
##    if out.split()[0] == "Error:":
##        issues.append((command, out))
##    else:
##        if command[0] == "effect" or command[0] == "modify":
##            inp = "save p tests\\" + command[2]
##            if len(command) >= 4:
##                inp += "_" + command[3]
##            inp += ".jpg"
##            print(inp)
##            print("reset p")
##if len(issues) == 0:
##    print("All worked fine.")
##else:
##    print("Some errors occured: \n")
##    for i in issues:
##        print(' '.join(i[0]))
##        print(i[1])
##        print()
        
        
