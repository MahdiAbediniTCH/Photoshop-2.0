from PIL import Image

def pic_flip(weight, height, img, img_pixels):
    for i in range(weight):
        for j in range(height-1,-1,-1):
              img.putpixel((weight-1-i,j), (img_pixels[i][j][0], img_pixels[i][j][1], img_pixels[i][j][2]))
    img.save("2.jpg")
    return

def pic_grey_scale(weight, height, img, img_pixels):
    for x in range(weight):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (int((r+g+b)/3),int((r+g+b)/3),int((r+g+b)/3)))
    img.save('2.jpg')


print("""welcome to photoshop 2.0 \na photoshop without any graphical interface""")

print("first, give us the adress of your photo")
photo_adress = input()

########img_pixels#########
img = Image.open(photo_adress)
weight = img.size[0]
height = img.size[1]
img_pixels = []
for x in range(weight):
    l = []
    for y in range(height):
        r, g, b = img.getpixel((x, y))
        l.append((r, g, b))
    img_pixels.append(l)
########img_pixels#########

print("use'modifications' or 'effects' fo further information")
type_of_input = input()
while(1):
    if type_of_input == "modifications":
        print("now choose \n'flip' 'rotate' 'crop'")
        type_of_modification = input()
        if type_of_modification == "flip":
            pic_flip(weight, height, img, img_pixels)
            print("is there any other edit you want to do? \n 'yes' or 'no'")
            yes_no = input()
            if yes_no == "no":
                break
            elif yes_no == "yes":
                pass
            else:
                print("unexpected input, please re-enter the input")
    elif type_of_input == "effects":
        print("now choose \n'black & white' 'colorify' 'brightness' 'grey scale' 'blur'")
        while(1):
            type_of_effect = input()
            if type_of_effect == "grey scale":
                pic_grey_scale(weight, height, img, img_pixels)
            else:
                print("unexpected input, please re-enter the input")
    else:
        print("the input was not expected, please re-enter your input")
        type_of_input = input()
