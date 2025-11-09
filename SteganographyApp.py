# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Signifigant Bit (LSB) encoding.

from PIL import Image

def numberToBinary(num):
    """Takes a base10 number and converts to a binary string with 8 bits"""
    return format(num, '08b')

def binaryToNumber(bin_str):
    """Takes a string binary value and converts it to a base10 integer."""
    return int(bin_str, 2)

def encode(img, msg):
    pixels = img.load()
    width, height = img.size
    msgLength = len(msg)

    if msgLength * 3 > width * height:
        raise ValueError("Image too small to hold this message.")

    # store length in first pixel’s red
    red, green, blue = pixels[0, 0]
    pixels[0, 0] = (msgLength, green, blue)

    letterSpot = 0
    pixel = 0

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = numberToBinary(ord(msg[letterSpot]))
            greenBinary = greenBinary[:7] + letterBinary[0]
            blueBinary = blueBinary[:7] + letterBinary[1]
        elif pixel % 3 == 1:
            redBinary = redBinary[:7] + letterBinary[2]
            greenBinary = greenBinary[:7] + letterBinary[3]
            blueBinary = blueBinary[:7] + letterBinary[4]
        else:
            redBinary = redBinary[:7] + letterBinary[5]
            greenBinary = greenBinary[:7] + letterBinary[6]
            blueBinary = blueBinary[:7] + letterBinary[7]
            letterSpot += 1

        pixels[x, y] = (
            binaryToNumber(redBinary),
            binaryToNumber(greenBinary),
            binaryToNumber(blueBinary),
        )
        pixel += 1

    img.save("secretImg.png", "PNG")

def decode(img):
    pixels = img.load()
    red, green, blue = pixels[0, 0]
    msgLength = red
    width, height = img.size

    msg = ""
    pixel = 0
    letterBinary = ""
    x = 0
    y = 0

    while len(msg) < msgLength:
        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = greenBinary[7] + blueBinary[7]
        elif pixel % 3 == 1:
            letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
        else:
            letterBinary += redBinary[7] + greenBinary[7] + blueBinary[7]
            msg += chr(binaryToNumber(letterBinary))
            letterBinary = ""

        pixel += 1
        x = pixel % width
        y = pixel // width

    return msg

def main():
    # To encode:
    # img = Image.open("pki.png")
    # msg = "This is a secret message I will hide in an image."
    # encode(img, msg)
    # img.close()

    # To decode:
    img = Image.open("secretImg.png")
    print(decode(img))

if __name__ == "__main__":
    main()
