from PIL import Image,ImageDraw,ImageFont,ImageChops

size=9
font = ImageFont.truetype("math2.ttf",size)
letters = [*"rf"]

pixels = {}

def checkIfPixelIsBlackEnough(color,threshold):
    return color[0]<threshold and color[1]<threshold and color[2]<threshold

for letter in letters:
    pixels[letter]={"points":[],"width":0,"height":size}

    k = Image.new("RGBA",(50,50),(255,255,255,255))
    d = ImageDraw.Draw(k)

    d.text((0,-1),letter,(0,0,0,255),font=font)
    k.save(f"image-{letter}.png")

    farthest = 0
    for x in reversed(list(range(50))):
        blackPointsInXRange=False
        for y in range(50):
            if checkIfPixelIsBlackEnough(k.getpixel((x,y)),200):
                blackPointsInXRange=True
                break
        if not blackPointsInXRange:
            farthest=x+1
    pixels[letter]["width"]=farthest

    for x in range(50):
        for y in range(50):
            if checkIfPixelIsBlackEnough(k.getpixel((x,y)),200):
                pixels[letter]["points"].append((x,y))

print(pixels)