#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
from PIL import Image
from io import BytesIO
import base64
import boto3
from generator.options.test_options import TestOptions
from PIL import Image
import torchvision.transforms as transforms
import logging, sys, os
from logging import handlers


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


def store2S3(env, filetype, userID, count, uni, upload_file):
    if filetype == 'bitmaps':
        #PIL to buffer
        buffer = BytesIO()
        upload_file.save(buffer, format='JPEG')
        upload_file = base64.b64encode(buffer.getvalue())

        contenttype = 'image/jpeg'
        body = base64.b64decode(upload_file)
    elif filetype == 'vectors':
        upload_file = open(upload_file, 'rb')

        contenttype = 'image/svg+xml'
        body = upload_file
    #just in case saving 'JPEG' file
    elif filetype == 'JPEG':
        upload_file = open(upload_file, 'rb')

        contenttype = 'image/jpeg'
        body = upload_file

    s3key = '%s/outputs/%s/%s/%s/%s' % (env, filetype, userID, count, uni)
    s3 = boto3.resource('s3')
    s3.Bucket('fontto').put_object(
        Key=s3key, Body=body, ContentType=contenttype, ACL='public-read')
    full_address = 'https://s3.ap-northeast-2.amazonaws.com/fontto/' + s3key
    return full_address


def ttf2S3(env, userID, count, ttf_converted):
    contenttype = 'font/ttf'
    body = ttf_converted

    s3key = '%s/outputs/ttf/%s/%s' % (env, userID, count)
    s3 = boto3.resource('s3')
    s3.Bucket('fontto').put_object(
        Key=s3key, Body=body, ContentType=contenttype, ACL='public-read')
    ttf_address = 'https://s3.ap-northeast-2.amazonaws.com/fontto/' + s3key
    return ttf_address


def woff2S3(env, userID, count, woff_converted):
    s3key = '%s/outputs/ttf/%s/%s' % (env, userID, count)
    logging.info(":: send [%s] to s3 [%s/] " % (woff_converted,
                                                's3://fontto/' + s3key))
    logging.info(":: [system call] aws s3 cp --acl public-read %s %s/" %
                 (woff_converted, s3key))
    os.system("aws s3 cp --acl public-read %s %s/" % (woff_converted,
                                                      's3://fontto/' + s3key))
    logging.info(":: [done system call]")
    woff_addr = 'https://s3.ap-northeast-2.amazonaws.com/fontto/' + s3key + "/" + woff_converted
    return woff_addr


def make_gen_opt():
    """
    - make default option for pix2pix model
    """
    opt = TestOptions().parse()
    opt.nThreads = 1  # test code only supports nThreads = 1
    opt.batchSize = 1  # test code only supports batchSize = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    return opt


def get_transform():
    transform_list = []
    transform_list += [
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ]
    return transforms.Compose(transform_list)


def pil2tensor(input_image):
    transform = get_transform()
    output_tensor = transform(input_image)
    return output_tensor


def set_logging(log_path):
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    log.addHandler(ch)

    fh = handlers.RotatingFileHandler(
        log_path, maxBytes=(1048576 * 5), backupCount=7)
    fh.setFormatter(format)
    log.addHandler(fh)

    logging.basicConfig(
        filename=log_path, datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
