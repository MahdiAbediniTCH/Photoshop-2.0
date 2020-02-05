from PIL import Image,ImageEnhance

def process(param, img):
    weight = img.size[0]
    height = img.size[1]
    img_pixels = []
    for x in range(weight):
        l = []
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            l.append((r, g, b))
        img_pixels.append(l)
    if param[0] == "brightness":
        print("Processing...")
        out = pic_brightness(weight, height, img, img_pixels, int(param[1]))
        print("Done")
        return 'image', out
    if param[0] == "flip":
        print("Processing...")
        pic_flip(weight, height, img, img_pixels, param[1])
        print("Done")
    elif param[0] == "rotate":
        print("Processing...")
        out = rotate(img, int(param[1]))
        print("Done")
        return 'image', out
    elif param[0] == "res_decrease":
        print("Processing...")
        for i in range(len(param)):
            param[i] = paranthesesOrComma(param[i])
        resdec(img, [[int(param[len(param)-4]),int(param[len(param)-3])], [int(param[len(param)-2]), int(param[len(param)-1])]], img_pixels)
        print("Done")
    else:
        return False,"attr"
    return True
    
def paranthesesOrComma(string):
    i = 0
    while i < len(string):
        if string[i] == "(" or string[i] == ")" or string[i] == ",":
            string = string[:i] + string[i+1:]
        i += 1
    return string

def pic_flip(weight, height, img, img_pixels, x_or_y):
    if x_or_y == "vertical":
        for i in range(weight):
            for j in range(height-1,-1,-1):
                  img.putpixel((weight-1-i,j), (img_pixels[i][j][0], img_pixels[i][j][1], img_pixels[i][j][2]))
    else:
        for k in range(2):
            for i in range(weight-1,-1,-1):
                for j in range(height-1,-1,-1):
                    img.putpixel((height-j-1,weight-i-1), (img_pixels[i][j][0], img_pixels[i][j][1], img_pixels[i][j][2]))
    return True

def pic_brightness(weight, height, img, img_pixels, zTOh_input):
    zTOh_input /= 50
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(zTOh_input)
    return img

def rotate(img, degree):
    img = img.rotate(degree)
    return img

def resdec(img, radius, img_pixels):
    for i in range(radius[0][0],radius[1][0],3):
        for j in range(radius[0][1], radius[1][1],3):
              rr = img_pixels[i][j][0]
              gg = img_pixels[i][j][1]
              bb = img_pixels[i][j][2]
              
              rr = int((img_pixels[i+1][j][0]+img_pixels[i+1][j][0]+img_pixels[i-1][j][0]+img_pixels[i][j+1][0]+img_pixels[i][j-1][0]+img_pixels[i+1][j+1][0]+img_pixels[i-1][j-1][0])/9)
              gg = int((img_pixels[i+1][j][1]+img_pixels[i+1][j][1]+img_pixels[i-1][j][1]+img_pixels[i][j+1][1]+img_pixels[i][j-1][1]+img_pixels[i+1][j+1][1]+img_pixels[i-1][j-1][1])/9)
              bb = int((img_pixels[i+1][j][2]+img_pixels[i+1][j][2]+img_pixels[i-1][j][2]+img_pixels[i][j+1][2]+img_pixels[i][j-1][2]+img_pixels[i+1][j+1][2]+img_pixels[i-1][j-1][2])/9)
              for k in range(-1,2):
                  for l in range(-1,2):
                      img.putpixel((i+k,j+l), (rr, gg, bb))
    return True
