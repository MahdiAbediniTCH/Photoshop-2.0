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
    modification = param[0]
    if modification == "brightness":
        print("Processing...")
        out = pic_brightness(weight, height, img, img_pixels, int(param[1]))
        print("Done")
        return 'image', out
    if modification == "crop":
        print("Processing...")
        out = crop(int(param[1]),int(param[2]) ,int(param[3]), int(param[4]), img)
        print("Done")
        return 'image', out
    if modification == "flip":
        print("Processing...")
        pic_flip(weight, height, img, img_pixels, param[1])
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
        resdec(img, [[int(param[len(param)-4]),int(param[len(param)-3])], [int(param[len(param)-2]), int(param[len(param)-1])]], img_pixels)
        print("Done")
    elif modification == "border":
        print("Processing...")
        bording(img, weight, height, img_pixels)
        print("Done")
    elif modification == "blur":
        print("Processing...")
        for i in range(len(param)):
            param[i] = paranthesesOrComma(param[i])
        if param[-1].isdecimal():
            if param[-1] in ['1','2','3']:
                blur(img, [[int(param[len(param)-5]),int(param[len(param)-4])], [int(param[len(param)-3]), int(param[len(param)-2])]], img_pixels, int(param[-1]))
            else:
                return False, 'lvl'
        else:
            blur(img, [[int(param[len(param)-4]),int(param[len(param)-3])], [int(param[len(param)-2]), int(param[len(param)-1])]], img_pixels, 1)
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
              rr = int((img_pixels[i+1][j][0]+img_pixels[i+1][j][0]+img_pixels[i-1][j][0]+img_pixels[i][j+1][0]+img_pixels[i][j-1][0]+img_pixels[i+1][j+1][0]+img_pixels[i-1][j-1][0])/9)
              gg = int((img_pixels[i+1][j][1]+img_pixels[i+1][j][1]+img_pixels[i-1][j][1]+img_pixels[i][j+1][1]+img_pixels[i][j-1][1]+img_pixels[i+1][j+1][1]+img_pixels[i-1][j-1][1])/9)
              bb = int((img_pixels[i+1][j][2]+img_pixels[i+1][j][2]+img_pixels[i-1][j][2]+img_pixels[i][j+1][2]+img_pixels[i][j-1][2]+img_pixels[i+1][j+1][2]+img_pixels[i-1][j-1][2])/9)
              for k in range(-1,2):
                  for l in range(-1,2):
                      img.putpixel((i+k,j+l), (rr, gg, bb))
    return True

def bording(img, weight, height, img_pixels):
    l = []
    ll = []
    sec_img_pixels = []
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
            flag = False
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

def blur(img, radius, pixels, lvl):

    for x in range(radius[0][0],radius[1][0]):
        for y in range(radius[0][1], radius[1][1]):
            sumr = sumg = sumb = 0
            count = 0
            for x2 in range(x - (2*lvl), x + 2*lvl + 1):
                if (radius[0][0] <= x2 < radius[1][0]):
                    for y2 in range(y - 2*lvl, y + 2*lvl + 1):
                        if (radius[0][1] <= y2 < radius[1][1]):
                            r, g, b = pixels[x2][y2]
                            sumr += r
                            sumg += g
                            sumb += b
                            count += 1
            avg = (sumr // count, sumg // count, sumb // count)
            img.putpixel((x, y), avg)

def crop(left, right, top, bottom, img): 
    img2 = img.crop((left, top, right, bottom))
    return img2
