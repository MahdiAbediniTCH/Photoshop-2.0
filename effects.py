from PIL import Image

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLACKWHITEVALUE = 0.7
COLOR_EFFECT_MEDIUM = 30
COLOR_MEDIUM = 255
COLOR_EFFECT_VALUES = {'red': (1, 0, 0), 'green': (0, 1, 0),\
    'blue': (0, 0, 1), 'yellow': (1 / 2, 1 / 2, 0),\
        'violet': (1 / 2, 0, 1 / 2)}

def process(param, img):
    effect = param[0]
    if effect == "grayscale":
        print("Processing...")
        grayscale(img)
        print("Done")
    elif effect == "color":
        print("Processing...")
        color(img, param[1])
        print("Done")
    elif effect == "colorfilter":
        print("Processing...")
        colorfilter(img, param[1])
        print("Done")
    elif effect == "negative":
        print("Processing...")
        negative(img)
        print("Done")
    elif effect == "whiteand":
        print("Processing...")
        whiteand(img, param)
        print("Done")
    else:
        return False, "attr"
    return True

def close_colors(c1, c2):
    r, g, b = [v1 - v2 for v1, v2 in zip(c1, c2)]
    return (r*r + g*g + b*b) <= 150*150

def get_hue(col):
    r, g, b = col
    mx = max(col)
    mn = min(col)
    if mx == mn or mx == 0:
        return None
    rp = (mx - r) / (mx - mn)
    gp = (mx - g) / (mx - mn)
    bp = (mx - b) / (mx - mn)
    if (r >= g and r >= b) and (g <= r and g <= b):
        h = 5 + bp
    elif (r >= g and r >= b):
        h = 1 - gp
    elif (g >= r and g >= b) and (b <= r and b <= g):
        h = rp + 1
    elif (g >= r and g >= b):
        h = 3 - bp
    elif (r >= g and r >= b):
        h = 3 + gp
    else:
        h = 5 - rp
    
    return h * 60
        

def calculate_brightness(rgb):
    return rgb[0] / 255 * 0.2126 + rgb[1] / 255 * 0.7152 + rgb[2] / 255 * 0.0722

def grayscale(img):
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            brightness_ = int(calculate_brightness(pixels[x,y]) * 255)
            img.putpixel((x,y), (brightness_, brightness_, brightness_))
    return True

def whiteand(img, param):
    pixels = img.load()
    if len(param) == 1:
        col = BLACK
    else:
        col = tuple([i*255 for i in COLOR_EFFECT_VALUES[param[1]]])
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            brightness_ = calculate_brightness(pixels[x,y])
            if brightness_ < BLACKWHITEVALUE:
                img.putpixel((x, y), col)
            else:
                img.putpixel((x, y), WHITE)
    return True

def negative(img):
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = pixels[x,y]
            r = 255 - r
            g = 255 - g
            b = 255 - b
            img.putpixel((x, y), (r, g, b))

def color(img, col):
    pixels = img.load()
    if type(col) == str:
        chosen_color = [int(v1 * COLOR_EFFECT_MEDIUM) for v1 in COLOR_EFFECT_VALUES[col]]
    else:
        chosen_color = col
    for x in range(img.size[0]):
       for y in range(img.size[1]):
           pixel_color = pixels[x,y]
           new_color = (pixel_color[0] + chosen_color[0], pixel_color[1] + chosen_color[1],\
               pixel_color[2] + chosen_color[2],)
           img.putpixel((x, y), new_color)
    return True

def colorfilter(img, col):
    pixels = img.load()
    chosen_color = [int(bool(v1) * 255) for v1 in COLOR_EFFECT_VALUES[col]]
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if get_hue(pixels[x,y]) == None:
                img.putpixel((x, y), tuple([int(calculate_brightness(pixels[x,y]) * 255)] * 3))
            elif not abs(get_hue(pixels[x,y]) - get_hue(chosen_color)) <= 20:
                img.putpixel((x, y), tuple([int(calculate_brightness(pixels[x,y]) * 255)] * 3))
