from PIL import Image,ImageEnhance
import math

def process(param, img):
    weight = img.size[0]
    height = img.size[1]
    modification = param[0]
    if modification == "temp":
        print("Processing")
        convert_temp(img, int(param[1]))
        print("Done")
    elif modification == "grad":
        print("Processing")
        out = grad(img, weight, height, param[1])
        print("Done")
        return 'image', out
    elif modification == "decrease_res":
        print("Processing...")
        res_dec(img, param[1])
        print("Done")
    elif modification == "brightness":
        print("Processing...")
        out = pic_brightness(img, int(param[1]))
        print("Done")
        return 'image', out
    elif modification == "crop":
        print("Processing...")
        out = crop(int(param[1]),int(param[2]) ,int(param[3]), int(param[4]), img)
        print("Done")
        return 'image', out
    elif modification == "flip":
        print("Processing...")
        pic_flip(weight, height, img, param[1])
        print("Done")
    elif modification == "rotate":
        print("Processing...")
        out = rotate(img, int(param[1]))
        print("Done")
        return 'image', out
    elif modification == "res_decrease":
        print("Processing...")
        for i in range(len(param)):
            param[i] = paranthesesOrComma(param[i])
        resdec(img, param)
        print("Done")
    elif modification == "border":
        print("Processing...")
        bording(img, weight, height)
        print("Done")
    elif modification == "blur":
        print("Processing...")
        for i in range(len(param)):
            param[i] = paranthesesOrComma(param[i])
        if param[5].isdecimal():
            if param[5] in ['1','2','3']:
                blur(img, param, int(param[5]))
            else:
                print(param[5])
                return False, 'lvl'
        else:
            blur(img, param, 1)
        print("Done")
    else:
        return False, "attr"
    return True
    
def paranthesesOrComma(string):
    i = 0
    while i < len(string):
        if string[i] == "(" or string[i] == ")" or string[i] == ",":
            string = string[:i] + string[i+1:]
        i += 1
    return string

def pic_flip(weight, height, img, x_or_y):
    img_pixels = img.load()
    if x_or_y == "vertical":
        for i in range(weight):
            for j in range(height-1,-1,-1):
                  img.putpixel((weight-1-i,j), (img_pixels[i,j][0], img_pixels[i,j][1], img_pixels[i,j][2]))
    else:
        for k in range(2):
            for i in range(weight-1,-1,-1):
                for j in range(height-1,-1,-1):
                    img.putpixel((height-j-1,weight-i-1), (img_pixels[i,j][0], img_pixels[i,j][1], img_pixels[i,j][2]))
    return True

def pic_brightness(img, zTOh_input):
    zTOh_input /= 50
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(zTOh_input)
    return img

def rotate(img, degree):
    img = img.rotate(degree)
    return img

def resdec(img, params):
    img_pixels = img.load()
    x1, y1 = int(params[1]), int(params[2])
    x2, y2 = int(params[3]), int(params[4])
    for i in range(x1, x2, 3):
        for j in range(y1, y2,3):
              rr = int((img_pixels[i+1,j][0]+img_pixels[i+1,j][0]+img_pixels[i-1,j][0]+img_pixels[i,j+1][0]+img_pixels[i,j-1][0]+img_pixels[i+1,j+1][0]+img_pixels[i-1,j-1][0])/9)
              gg = int((img_pixels[i+1,j][1]+img_pixels[i+1,j][1]+img_pixels[i-1,j][1]+img_pixels[i,j+1][1]+img_pixels[i,j-1][1]+img_pixels[i+1,j+1][1]+img_pixels[i-1,j-1][1])/9)
              bb = int((img_pixels[i+1,j][2]+img_pixels[i+1,j][2]+img_pixels[i-1,j][2]+img_pixels[i,j+1][2]+img_pixels[i,j-1][2]+img_pixels[i+1,j+1][2]+img_pixels[i-1,j-1][2])/9)
              for k in range(-1,2):
                  for l in range(-1,2):
                      img.putpixel((i+k,j+l), (rr, gg, bb))
    return True

def bording(img, weight, height):
    l = []
    ll = []
    sec_img_pixels = []
    img_pixels = []
    for i in range(weight):
        temp = []
        for j in range(height):
            temp.append(img.getpixel((i, j)))
        img_pixels.append(temp)
        del temp
    for i in range(len(img_pixels)):
        for j in range(len(img_pixels[i])):
            for k in range(len(img_pixels[i][j])):
                l.append(img_pixels[i][j][k])
            ll.append(l)
            l = []
        sec_img_pixels.append(ll)
        ll = []
    for i in range(2,weight-2):
        for j in range(2,height-2):
            jam0 = jam1 = jam2 = jam3 = 0
            xs = [i+1, i-1]
            ys = [j+1, j-1]
            for k in range(3):
                jam0 += abs(img_pixels[i+1][j+1][k] - img_pixels[i-1][j-1][k])
                jam1 += abs(img_pixels[i+1][j][k] - img_pixels[i-1][j][k])
                jam2 += abs(img_pixels[i-1][j][k] - img_pixels[i+1][j][k])
                jam3 += abs(img_pixels[i][j-1][k] - img_pixels[i][j+1][k])
            
            if jam0 > 120 or jam1 > 120 or jam2 > 120 or jam3 > 120:
                sec_img_pixels[xs[0]][ys[0]][0] = sec_img_pixels[xs[0]][ys[0]][1] = sec_img_pixels[xs[0]][ys[0]][2] = 255
            else:
                sec_img_pixels[xs[0]][ys[0]][0] = sec_img_pixels[xs[0]][ys[0]][1] = sec_img_pixels[xs[0]][ys[0]][2] = 0
            

    for i in range(weight):
        for j in range(height):
            img.putpixel((i,j), (sec_img_pixels[i][j][0], sec_img_pixels[i][j][1], sec_img_pixels[i][j][2]))

def blur(img, param, lvl):
    pixels = img.load()
    x1, y1 = int(param[1]), int(param[2])
    x2, y2 = int(param[3]), int(param[4])
    for x in range(min(x1, x2), max(x1, x2)):
        for y in range(min(y1, y2), max(y1, y2)):
            sumr = sumg = sumb = 0
            count = 0
            for xx in range(x - (2*lvl), x + 2*lvl + 1):
                if (x1 <= xx < x2):
                    for yy in range(y - 2*lvl, y + 2*lvl + 1):
                        if (y1 <= yy < y2):
                            r, g, b = pixels[xx,yy]
                            sumr += r
                            sumg += g
                            sumb += b
                            count += 1
            avg = (sumr // count, sumg // count, sumb // count)
            img.putpixel((x, y), avg)

def crop(left, right, top, bottom, img): 
    img2 = img.crop((left, top, right, bottom))
    return img2

def res_dec(img, rad):
    to_tagh = 1
    if int(rad) == 1:
        to_tagh = 4
    if int(rad) == 2:
        to_tagh = 3
    if int(rad) == 3:
        to_tagh = 2
    x,y = img.size
    x2,y2 = math.floor(int(x/to_tagh)), math.floor(int(y/to_tagh))
    img2 = img.resize((x2,y2), Image.ANTIALIAS)
    return img2

def grad(img, weight, height, color):
    for i in range (height):
        for j in range(weight):
            r, g, b = img.getpixel((i, j))
            if color == "blue":
                img.putpixel((i, j), (0, 0, b))
            elif color == "red":
                img.putpixel((i, j), (r, 0, 0))
            elif color == "green":
                img.putpixel((i, j), (0, g, 0))
            elif color == "violet":
                img.putpixel((i,j), (r,0,b))
            elif color == "grey":
                img.putpixel((i,j), ((r+g+b)/3, (r+g+b)/3, (r+g+b)/3)) 
    return img

def convert_temp(image, temp):
    weight, height = image.size
    for i in range(weight):
        for j in range(height):
            r, g, b = image.getpixel((i,j))
            image.putpixel((i, j), (r+temp, g, b-temp))
    return image

##img = Image.open("pic.jpg")
##process(["temprature", -50], img)
