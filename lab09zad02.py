from PIL import Image, ImageFont, ImageDraw
from os.path import exists
import textwrap


def decode_image(file_location="images/encoded_sample.png"):

    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size, y_size, bump = encoded_image.size[0], encoded_image.size[1], 0
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)

    file_exists = exists("images/decoded_image.png")
    while file_exists is True:
        bump += 1
        file_exists = exists("images/decoded_image" + str(bump) + ".png")
        if file_exists is False:
            decoded_image.save("images/decoded_image" + str(bump) + ".png")
    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, image_size):

    imgtext = Image.new("RGB", image_size)
    font, drawer = ImageFont.load_default().font, ImageDraw.Draw(imgtext)
    margin = offset = 10

    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return imgtext


def encode_image(text_to_encode, tempimg="images/zamek.png"):

    tempimg = Image.open(tempimg)
    redtemp, greentemp, bluetemp = tempimg.split()[0], tempimg.split()[1], tempimg.split()[2]

    x_size, y_size = tempimg.size[0], tempimg.size[1]
    imgtext = write_text(text_to_encode, tempimg.size)
    drawtext = imgtext.convert('1')
    encoded_image = Image.new("RGB", (x_size, y_size))
    pixels = encoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            redpix = bin(redtemp.getpixel((i, j)))
            encodepix = bin(drawtext.getpixel((i, j)))

            if encodepix[-1] != '1':
                redpix = redpix[:-1] + '0'
            else:
                redpix = redpix[:-1] + '1'
            pixels[i, j] = (int(redpix, 2), greentemp.getpixel((i, j)), bluetemp.getpixel((i, j)))
    encoded_image.save("images/encoded_sample.png")


decode_image()
encode_image("To jest zamek taki!")
