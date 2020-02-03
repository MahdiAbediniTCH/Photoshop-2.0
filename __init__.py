from PIL import Image
from sys import stderr
import effects
import modifications

ERRORS = {'?': "An error occured", 'q': "Invalid use of quotation mark", 'attr': "Invalid attribute", \
    'command': "Invalid command", 'name': "Name not found", \
        'lack': "Lack of parameters", 'file': "File not found"}

def error(key):
    print("Error:", ERRORS[key], file=stderr)
    return

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
        if part[-1] == '"':
            if not quote_open: return False, "q"
            quote_open = False
            quote[-1] = quote[-1][:-1]
            res.append(' '.join(quote))
    return res

def main():
    pictures = {}

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
            except FileNotFoundError:
                error('file')
            except IndexError:
                error('lack')
            except:
                error('?')
        elif command == "effect":
            try:
                res = effects.process(param[2:], pictures[param[1]])
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
                res = modifications.process(param[2:], pictures[param[1]])
            except KeyError:
                error('name')
                continue
            except Exception as e:
                error('?')
                raise e
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
            except KeyError:
                error('name')
            except:
                error('?')
        elif command == "exit":
            return True
        else:
            error('command')

if __name__ == "__main__":
    main()
