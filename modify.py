#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageChops, ImageOps


def scale(image, max_size, method=Image.ANTIALIAS):
    im_aspect = float(image.size[0]) / float(image.size[1])
    out_aspect = float(max_size[0]) / float(max_size[1])
    if im_aspect >= out_aspect:
        scaled = image.resize(
            (max_size[0], int((float(max_size[0]) / im_aspect) + 0.5)), method)
    else:
        scaled = image.resize(
            (int((float(max_size[1]) * im_aspect) + 0.5), max_size[1]), method)

    offset = (int((max_size[0] - scaled.size[0]) / 2), int(
        (max_size[1] - scaled.size[1]) / 2))
    # print(offset)
    back = Image.new("RGB", max_size, "white")
    back.paste(scaled, offset)
    return back


def trim_resize_PIL(input_PIL, width, height, border):
    bg = Image.new(input_PIL.mode, input_PIL.size, input_PIL.getpixel((0, 0)))
    diff = ImageChops.difference(input_PIL, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    image_output = input_PIL.crop(bbox)
    image_output = scale(image_output, [width, height])
    image_output = ImageOps.expand(image_output, border=border, fill='white')
    return image_output


def noise_filter(PIL_img):
    """
    IF use convertio, THEN just pass out the input
    ELSE, take PIL image and return PIL image
    """
    modified_PIL = "modified_PIL"
    return modified_PIL


def vectoralize(PIL_img):
    """
    take PIL, convert to JPG, pass through convertio API, return 'path/name.svg'
    """
    vectored_PIL = "./assets/sample.svg"  #원래는 생성된 .svg 파일이 들어가야
    return vectored_PIL


def svgs2ttf(svg_set):
    """
    go through hash 'svg_set', read each unicode & svgfile, compine all to one ttf file and return single ttf file
    """
    ttf_converted = "user_count.ttf"
    return ttf_converted
