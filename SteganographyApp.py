# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Signifigant Bit (LSB) encoding.

from PIL import Image
import os

def encode(img, msg):
  #TODO: You need to convert the RGB to binary
  #Then we will adjust the pixels to encode the message binary value into the last bit.
  #Each letter will take three pixels, with a spare pixel unchanged.
  pixels = img.load() # pixesls is the pixel map, 2-d list of data
  width, height = img.size
  letterSpot = 0
  pixel = 0
  letterBinary = ""
  msgLength = len(msg)
  red, green, blue = pixels[0, 0]
  pixels[0,0] = (msgLength, green, blue)

  for i in range(msgLength * 3):
    x = i % width
    y = i // width

    red, green, blue = pixels[x, y]
    redBinary = numberToBinary(red)
    greenBinary = numberToBinary(green)
    blueBinary = numberToBinary(blue)

    if pixel % 3 == 0:
      letterBinary = numberToBinary(ord(msg[letterSpot]))
      #ignore the red on the first pixel of each letter.
      greenBinary = greenBinary[0:7] + letterBinary[0]
      blueBinary = blueBinary[0:7] + letterBinary[1]
    elif pixel % 3 == 1:
      redBinary = redBinary[0:7] + letterBinary[2]
      greenBinary = greenBinary[0:7] + letterBinary[3]
      blueBinary = blueBinary[0:7] + letterBinary[4]
    else:
      redBinary = redBinary[0:7] + letterBinary[5]
      greenBinary = greenBinary[0:7] + letterBinary[6]
      blueBinary = blueBinary[0:7] + letterBinary[7]

      letterSpot = letterSpot + 1

    red = binaryToNumber(redBinary)
    blue = binaryToNumber(blueBinary)
    green = binaryToNumber(greenBinary)

    pixels[x,y] = (red, green, blue)
    pixel = pixel + 1

  #Save the file that has now been encoded.
  img.save("secretImg.png", 'png')

def decode(img):
  """Takes the image file and reads the least significant bit from the RGBA channels.
  Converts that binary to decimal to ASCII."""
  msg = ""

  pixels = img.load() #Pixels is the pixel map, a 2-dimensional list of pixel data
  red,green,blue = pixels[0,0]
  msgLength = red
  width, height = img.size
  letterSpot = 0
  pixel = 0
  letterBinary = ""
  x = 0
  y = 0
  while len(msg) < msgLength:
    red,green,blue = pixels[x,y]
    redBinary = numberToBinary(red)
    greenBinary = numberToBinary(green)
    blueBinary = numberToBinary(blue)

    if pixel % 3 == 0:
      letterBinary = greenBinary[7] + blueBinary[7]

    elif pixel % 3 == 1:
      letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]

    else:
      letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]
      letterAscii = binaryToNumber(letterBinary)
      letter = chr(letterAscii)
      msg = msg + chr(letterAscii)

    pixel = pixel + 1
    x = pixel % width
    y = pixel // width

  return msg

#Helper functions

def numberToBinary(num):
  """Takes a base10 number and converts to a binary string with 8 bits"""
  binary = ""
  #Convert from decimal to binary


  return binary

def binaryToNumber(bin):
  """Takes a string binary value and converts it to a base10 integer."""
  decimal = 0


  return decimal

def main():
  #Ask user if they want to encode/decode
  myImg = Image.open('pki.png')
  myMsg = "This is a secret message I will hide in an image."
  encode(myImg, myMsg)
  myImg.close()

  """
  yourImg = Image.open('secretImg.png')
  msg = decode(yourImg)
  print(msg)
  """
    
if __name__ == '__main__':
  main()
