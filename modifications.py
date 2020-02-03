from PIL import Image,ImageEnhance

def process(param, image):
    img = Image.open(image)
    weight = img.size[0]
    height = img.size[1]
    img_pixels = []
    for x in range(weight):
        l = []
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            l.append((r, g, b))
        img_pixels.append(l)
    
    if param[0] == "pic_flip":
        pic_flip(weight, height, img, img_pixels, param[len(param)-1])
    if param[0] == "rotate":
        roatae(img, param[len(param-1)])
    if param[0] == "blur":
        blur(img, [[param[len(param)-4],param[len(param)-3]], [param[len(param)-2],param[len(param)-1]], img_pixels])
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
    if x_or_y == "horizontal":
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
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(zTOh_input)
    return True

def rotate(img, degree):
    img = img.rotate(degree)
    return True

def blur(img, radius, img_pixels):
    for i in range(radius[0][0],radius[1][0],3):
        for j in range(radius[0][1], radius[1][1],3):
              rr = img_pixels[i][j][0]
              gg = img_pixels[i][j][1]
              bb = img_pixels[i][j][2]
              if i<weight-3 and j<height-3 and i>2 and j>2:
                  rr = int((img_pixels[i+1][j][0]+img_pixels[i+1][j][0]+img_pixels[i-1][j][0]+img_pixels[i][j+1][0]+img_pixels[i][j-1][0]+img_pixels[i+1][j+1][0]+img_pixels[i-1][j-1][0])/9)
                  gg = int((img_pixels[i+1][j][1]+img_pixels[i+1][j][1]+img_pixels[i-1][j][1]+img_pixels[i][j+1][1]+img_pixels[i][j-1][1]+img_pixels[i+1][j+1][1]+img_pixels[i-1][j-1][1])/9)
                  bb = int((img_pixels[i+1][j][2]+img_pixels[i+1][j][2]+img_pixels[i-1][j][2]+img_pixels[i][j+1][2]+img_pixels[i][j-1][2]+img_pixels[i+1][j+1][2]+img_pixels[i-1][j-1][2])/9)
                  for k in range(-1,2):
                      for l in range(-1,2):
                          img.putpixel((i+k,j+l), (rr, gg, bb))
    return True
