from PIL import Image
from sys import stderr
import effects, modifications
import copy

ERRORS = {'?': "An error occured", 'q': "Invalid use of quotation mark", 'attr': "Invalid attribute", \
    'command': "Invalid command", 'name': "Name not found", \
        'lack': "Lack of parameters", 'file': "File not found"}

def help_():
    file = open("help.txt", 'r')
    print(file.read())

def error(key):
    if key == None:
        return
    print("Error:", ERRORS[key], file=stderr)
    return

def get_parameters(string):
    splitted = string.split()
    if len(splitted) == 0:
        return False, None
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
        if part[-1] == '"':
            if not quote_open: return False, "q"
            quote_open = False
            quote[-1] = quote[-1][:-1]
            res.append(' '.join(quote))
    return res

def main():
    help_()
    pictures = {}
    original_pictures = {}
    undo = {}
    while True:
        param = get_parameters(input())
        if type(param) == tuple:
            if param[0] == False:
                error(param[1])
                continue
        command = param[0]
        
        if command == "open":
            try:
                pictures[param[2]] = Image.open(param[1])
                original_pictures[param[2]] = Image.open(param[1])
            except FileNotFoundError:
                error('file')
            except IndexError:
                error('lack')
            except:
                error('?')

        elif command == "effect":
            try:
                undo[param[1]] = copy.deepcopy(pictures[param[1]])
                res = effects.process(param[2:], pictures[param[1]])
                if type(res) == tuple:
                    if res[0] == False:
                        del undo[param[1]]
                        if res[1] == 'attr':
                            error('attr')
                            continue
            except KeyError:
                error('name')
                continue
            except:
                error('?')
                continue
            if type(res) == tuple:
                if not res[0]:
                    error(res[1])
                    continue

        elif command == "modify":
            try:
                undo[param[1]] = copy.deepcopy(pictures[param[1]])
                res = modifications.process(param[2:], pictures[param[1]])
                if type(res) == tuple:
                    if res[0] == False:
                        del undo[param[1]]
                        if res[1] == 'attr':
                            error('attr')
                            continue
            except KeyError:
                error('name')
                continue
            except:
                error('?')
                continue
            if type(res) == tuple:
                if not res[0]:
                    error(res[1])
                    continue
                if res[0] == 'image':
                    pictures[param[1]] = res[1]

        elif command == "save":
            try:
                pictures[param[1]].save(param[2])
            except KeyError:
                error('name')
            except:
                error('?')

        elif command == "close":
            try:
                del pictures[param[1]]
                del original_pictures[param[1]]
            except KeyError:
                error('name')
            except:
                error('?')
            
        elif command == "reset":
            try:
                pictures[param[1]] = original_pictures[param[1]]
            except KeyError:
                error('name')
            except:
                error('?')
        elif command == "undo":
            try:
                pictures[param[1]] = undo[param[1]]
                del undo[param[1]]
            except KeyError:
                print("There is no undo point for this image")
            except:
                error('?')
            
        elif command == "images":
            if len(pictures) == 0:
                print("There are no open images")
                continue
            for key in pictures:
                print(f"{key}: {pictures[key].filename}")

        elif command == "help":
            help_()

        elif command == "exit":
            return True
        
        elif command == "show":
            pictures[param[1]].show()

        else:
            error('command')
        

if __name__ == "__main__":
    main()
