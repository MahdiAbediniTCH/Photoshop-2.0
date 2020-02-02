import effects
from PIL import Image
#import modifications

ERRORS = {'q': "Error: Invalid use of quotation mark"}

def get_parameters(string):
    splitted = string.split()
    quote_open = False
    res = []
    for part in splitted:
        if quote_open:
            quote.append(part)
        else:
            res.append(part)
        if part[0] == '"':
            if quote_open: return False, "q"
            res.pop()
            quote_open = True
            quote = [part[1:]]
        elif part[-1] == '"':
            if not quote_open: return False, "q"
            quote_open = False
            quote[-1] = quote[-1][:-1]
            res.append(' '.join(quote))
    return res

pictures = {}

while True:
    param = get_parameters(input())
    command = param[0]
    if command == "open":
        pictures[param[2]] = Image.open(param[1])
    elif command == "effect":
        effects.process(param[1:], pictures[param[1]])
    elif command == "modify":
        modifications.process(param[1:], pictures[param[1]])
    elif command == "save":
        pictures[param[1]].save(param[2])
    elif command == "close":
        del pictures[param[1]]
    
        
