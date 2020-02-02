from PIL import Image

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLACKWHITEVALUE = 0.7
COLOR_MEDIUM = 50
COLOR_EFFECT_VALUES = {'red': (COLOR_MEDIUM, 0, 0), 'green': (0, COLOR_MEDIUM, 0),\
    'blue': (0, 0, COLOR_MEDIUM), 'yellow': (COLOR_MEDIUM // 2, COLOR_MEDIUM // 2, 0),\
        'violet': (COLOR_MEDIUM // 2, 0, COLOR_MEDIUM // 2)}

def process(param, img):
    if param[0] == "grayscale":
        grayscale(img)
    elif param[0] == "blackandwhite":
        blackandwhite(img)
    elif param[0] == "color":
        color(img, param[1])
    else:
        return False, "attr"
    return True

def calculate_brightness(rgb):
    return rgb[0] / 255 * 0.2126 + rgb[1] / 255 * 0.7152 + rgb[2] / 255 * 0.0722

def grayscale(img):
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            brightness_ = int(calculate_brightness(pixels[x,y]) * 255)
            img.putpixel((x,y), (brightness_, brightness_, brightness_))
    return True

def blackandwhite(img):
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            brightness_ = calculate_brightness(pixels[x,y])
            if brightness_ < BLACKWHITEVALUE:
                img.putpixel((x, y), BLACK)
            else:
                img.putpixel((x, y), WHITE)
    return True

def color(img, col):
    pixels = img.load()
    if type(col) == str:
        chosen_color = COLOR_EFFECT_VALUES[col]
    else:
        chosen_color = col
    for x in range(img.size[0]):
       for y in range(img.size[1]):
           pixel_color = pixels[x,y]
           new_color = (pixel_color[0] + chosen_color[0], pixel_color[1] + chosen_color[1],\
               pixel_color[2] + chosen_color[2],)
           img.putpixel((x, y), new_color)
    return True
