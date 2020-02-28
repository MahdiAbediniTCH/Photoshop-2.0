from PIL import Image
from sys import stderr
import effects, modifications
import copy

ERRORS = {'?': "An error occured", 'q': "Invalid use of quotation mark", 'attr': "Invalid attribute", \
    'command': "Invalid command", 'name': "Name not found", \
        'lack': "Lack of parameters", 'file': "File not found", 'lvl': "Invalid level", 'img_ind': "Image index out of range", \
          }

def help_(params, pictures, original_pictures, undo):
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
        return False
    quote_open = False
    res = []
    for part in splitted:
        if quote_open:
            quote.append(part)
        else:
            res.append(part)
        if part[0] == '"':
            if quote_open:
                error('q')
                return False
            res.pop()
            quote_open = True
            quote = [part[1:]]
        if part[-1] == '"':
            if not quote_open:
                error('q')
                return False
            quote_open = False
            quote[-1] = quote[-1][:-1]
            res.append(' '.join(quote))
    return res

def open_image(params, pictures, original_pictures, undo):
    try:
        pictures[params[2]] = Image.open(params[1])
        original_pictures[params[2]] = Image.open(params[1])
    except FileNotFoundError:
        error('file')
    except IndexError:
        error('lack')
    except:
        error('?')

def effect(params, pictures, original_pictures, undo):
    name = params[1]
    try:
        undo[name] = copy.deepcopy(pictures[name])
        res = effects.process(params[2:], pictures[name])
        if type(res) == tuple:
            if res[0] == False:
                del undo[name]
                if res[1] == 'attr':
                    error('attr')
    except KeyError:
        error('name')
    except:
        error('?')

def modify(params, pictures, original_pictures, undo):
    name = params[1]
    try:
        undo[name] = copy.deepcopy(pictures[name])
        res = modifications.process(params[2:], pictures[name])
        if type(res) == tuple:
            if res[0] == False:
                del undo[name]
                print(res)
                error(res[1])
            elif res[0] == 'image':
                pictures[name] = res[1]
    except KeyError:
        error('name')
    except IndexError as e:
        if str(e) == "image index out of range":
            error('img_ind')
        else:
            error('lack')
    except Exception as e:
        raise e
        error('?')

def save(params, pictures, original_pictures, undo):
    name = params[1]
    try:
        pictures[name].save(params[2])
    except KeyError:
        error('name')
    except:
        raise e
        error('?')    

def close(params, pictures, original_pictures, undo):
    name = params[1]
    try:
        del pictures[name]
        del original_pictures[name]
        if name in undo.keys():
            del undo[name]
    except KeyError:
        error('name')
    except:
        error('?')

def reset(params, pictures, original_pictures, undo):
    name = params[1]
    try:
        undo[name] = copy.deepcopy(pictures[name])
        pictures[name] = original_pictures[name]
    except KeyError:
        del undo[name]
        error('name')
    except:
        del undo[name]
        error('?')

def undo(params, pictures, original_pictures, undo):
    try:
        name = params[1]
        pictures[name] = undo[name]
        del undo[name]
    except KeyError:
        name = params[1]
        if not (name in pictures.keys()):
            error('name')
        else:
            print("There is no undo point for this image")
    except:
        error('?')

def list_images(params, pictures, original_pictures, undo):
    if len(pictures) == 0:
        print("There are no open images")
##    else:        
##        for key in pictures:
##            print(%s: %s".format(key, pictures[key].filename")

def show_image(params, pictures, original_pictures, undo):
    name = params[1]
    try:
        pictures[name].show()
    except KeyError:
        error('name')

COMMANDS = {'open': open_image, 'effect': effect, 'modify': modify, 'save': save, 'close': close, \
            'reset': reset, 'undo': undo, 'images': list_images, 'show': show_image}

def process_command(command, params, pictures, original_pictures, undo):
    try:
        COMMANDS[command](params, pictures, original_pictures, undo)
    except KeyError:
        error('command')

def main():
    help_(0, 0, 0, 0)
    pictures = {}
    original_pictures = {}
    undo = {}
    while True:
        param = get_parameters(input())
        if not param:
            continue
        command = param[0]
        if command == "exit":
            return True

        process_command(command, param, pictures, original_pictures, undo)
        
if __name__ == "__main__":
    main()
