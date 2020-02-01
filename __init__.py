import effects
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
print(get_parameters(input()))

        
