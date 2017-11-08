#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
from PIL import Image
from io import BytesIO


def url2img(input_address):
    """
    - fontto_pix2pix에서 사용할 수 있도록 url을 통해 이미지를 로드하고 PIL Image로 변환하여 반환
    - 입력 : url
    - 반환 : image
    """
    # url -> bytes
    url = urllib.parse.urlsplit(input_address)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    url = urllib.request.urlopen(url).read()
    bytesFromS3 = BytesIO(url)
    # bytes -> image
    input_PIL = Image.open(bytesFromS3)

    return input_PIL


def store2S3(userID, count, uni, PIL, env, s3key):
    full_address = "full address of img stored in S3"
    return full_address


def ttf2S3(userID, count, ttf_converted, env):
    ttf_address = "ttf address saved in S3"
    return ttf_address
