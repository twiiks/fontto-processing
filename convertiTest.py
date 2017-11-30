#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import urllib.parse
import urllib.request
from urllib.request import urlopen
from io import BytesIO
import io
from PIL import Image
import base64
import requests
import json



def url2img(input_address):
    """
    - fontto_pix2pix에서 사용할 수 있도록 url을 통해 이미지를 로드하고 PIL Image로 변환하여 반환
    - 입력 : url
    - 반환 : image (현재 base64 form 으로 받음)
    - jpg 들을 list 로 보내서 한번에 변환 할 수 있으며, 아직 테스트해보지 않음
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

    print("url2img done\n----------")
    return input_PIL


def convertio(convert_PIL):
    #change PIL -> base64
    buffer = BytesIO()
    convert_PIL.save(buffer, format='JPEG')
    convert_base64 = base64.b64encode(buffer.getvalue())

    #POST base64 for conversion
    url_post_base64 = 'https://api.convertio.co/convert'
    params_post = {'apikey': os.environ["CONVERTIO_TOKEN"], 
                   'input': 'base64', 
                   'file': convert_base64.decode("utf-8"), 
                   'filename': 'BD00.jpg',
                   'outputformat': 'svg'}
    req_post_base64 = requests.post(url_post_base64, data=json.dumps(params_post))
    print(req_post_base64.status_code)
    print(req_post_base64.text)
    print("post base64 file done\n----------")

    #GET conversion status
    res_post_base64 = json.loads(req_post_base64.text)
    url_get_status = 'https://api.convertio.co/convert/' + res_post_base64['data']['id'] + '/status'
    print(url_get_status)
    params_get = { 'id': res_post_base64['data']['id'] }
    req_get_status = requests.get(url_get_status, params = params_get)
    print(req_get_status.status_code)
    print(req_get_status.text)
    print("get status done\n----------")

    #GET result file
    url_get_base64 = 'http://api.convertio.co/convert/' + res_post_base64['data']['id'] + '/dl/' + 'base64'
    params_get = {'id': res_post_base64['data']['id']}
    req_get_result = requests.get(url_get_base64, params = params_get)
    print(req_get_result.status_code)
    print(req_get_result.text)
    res_get_base64 = json.loads(req_get_result.text)
    converted_base64 = res_get_base64['data']['content']

#    #result base64 -> PIL
#    """ not completed yet """
#    buf = base64.b64decode(converted_base64)
#    buf = io.BytesIO(buf)
#    output_PIL = Image.open(buf)
    
    

#    #Call-back url
#    url_post_result = 'https://api.convertio.co/convert'
#    params_post = {'id': res_post_base64['data']['id'],
#                    'step': 'finished'}
#    req_post_result = requests.post(url_post_result, data=json.dumps(params_post))
#    print(req_post_result.status_code)
#    print(req_post_result.text)

    print("convertio done")
#    return output_PIL


convert_PIL = url2img("https://s3.ap-northeast-2.amazonaws.com/fontto/development/outputs/bitmaps/seo/0/B9D0")
convertio(convert_PIL)
