#!/usr/bin/python3
# -*- coding: utf-8 -*-
from written2all import written2all
from utils import url2img, store2S3, ttf2S3, make_gen_opt, set_logging, woff2S3
from modify import trim_resize_PIL, noise_filter, vectoralize, svgs2ttf, resize_trim_PIL, vectoralize_potrace
import logging


def is_demo_v2(unicodes):
    DEMO_UNICODES = ["B053", "B294", "B77C", "BA74"]
    DEMO_UNICODES.sort()
    unicodes.sort()
    return True

#received_message -> processing -> output
def back_processing(userID, count, unicodes, env):
    logging.info("-----START BACKPROCESSING for userID: %s, count: %s-----" %
                 (userID, count))
    #INITIALIZE HASH: {'unicode': 'PIL_imgs'} (TTF 변환을 위한 hash)
    svg_set = []
    opt = make_gen_opt()
    is_demo = is_demo_v2(unicodes)
    logging.info(":: demo version [%s] ::" % is_demo)

    #FOR each unicode IN unicodes (입력받은 각각의 글자에 대해 아래 작업 수행)
    for input_unicode in unicodes:
        logging.info("-----process for INPUT_UNICODE: %s" % input_unicode)
        #get img_url from S3 WITH userID, count, unicode (입력값을 통해 S3에 있는 글자 주소 선언)
        s3key_input = '%s/inputs/%s/%s/%s' % (env, userID, count, input_unicode)
        input_address = 'https://s3.ap-northeast-2.amazonaws.com/fontto/' + s3key_input + '.jpg'

        logging.info("url2img for %s" % input_unicode)
        #url2img(url): url_img -> PIL_img
        try:
            input_PIL = url2img(input_address)
        except Exception as e:
            #if url2img fails to open input_address, it raises an error
            logging.error("[%s] : url ' %s '을 열 수 없습니다." % (e, input_address))
            continue

        logging.info("trim_resize_PIL for %s" % input_unicode)
        #trim_resize_PIL(PIL, width, height, border): trim PIL_img
        modified_PIL = trim_resize_PIL(input_PIL, 216, 216, 20)

        #store2S3(env, filetype, userID, count, input_unicode, modified_PIL): save output BITMAPS of input image
        filetype = 'bitmaps'
        # logging.info("save input bitmap PIL on S3 for %s" % input_unicode)
        # store2S3(env, filetype, userID, count, input_unicode, modified_PIL)


        #written2all(unicode, PIL_img): single PIL_img to multi PIL_imgs
        logging.info("written2all for %s" % input_unicode)
        output_images = written2all(input_unicode, modified_PIL, opt, is_demo,
                                    unicodes)
        logging.info("SAME CLASS WITH unicode: %s are %s" % (input_unicode,
                                                             output_images))

        #FOR each PIL_img IN PIL_imgs
        for output_unicode, output_image in output_images.items():
            logging.info("-----process for OUTPUT_UNICODE: %s" % output_unicode)
            #store2S3(env, filetype, userID, count, output_unicode, output_image): save PIL_imgs to S3
            filetype = 'bitmaps'
            # logging.info("save output bitmap PIL on S3 for %s" % output_unicode)
            # store2S3(env, filetype, userID, count, output_unicode, output_image)

            #noise_filter(PIL_img): noise reduction
            logging.info("reducting output noise for %s" % output_unicode)
            filterd = noise_filter(output_image)

            #resize_trim_PIL(input_PIL, width, height, border): resize and then trim PIL image
            logging.info("resize_trim_PIL for %s" % output_unicode)
            filterd = resize_trim_PIL(filterd, 800, 1000, 0)

            #vectoralize_potrace(PIL_img, unicode): vectoralize PIL_img
            logging.info("vectoralize output PIL for %s" % output_unicode)
            vectoralized = vectoralize_potrace(filterd, output_unicode)
            #APPEND vectoralized PIL_img to HASH
            svg_set.append(vectoralized)

            #store2S3(env, filetype, userID, count, output_unicode, vectoralized): save vectoralized image to vectors-S3
            filetype = 'vectors'
            logging.info(
                "save vectoralized output PIL on S3 for %s" % output_unicode)
            # store2S3(env, filetype, userID, count, output_unicode, vectoralized)

        #resize_trim_PIL(input_PIL, width, height, border): resize and then trim PIL image
        logging.info("resize_trim_PIL for %s" % input_unicode)
        modified_PIL = resize_trim_PIL(modified_PIL, 800, 1000, 0)

        #vectoralize_potrace(PIL_img, unicode): vectoralize user img
        logging.info("vectoralize input PIL for %s" % input_unicode)
        vectored_svg = vectoralize_potrace(modified_PIL, input_unicode)
        #APPEND vectoralized user img to HASH
        svg_set.append(vectored_svg)

        #store2S3(env, filetype, userID, count, input_unicode, vectored_svg): save vectoralized image to vectors-S3
        filetype = 'vectors'
        # logging.info("save vectoralized input PIL on S3 for %s" % input_unicode)
        # store2S3(env, filetype, userID, count, input_unicode, vectored_svg)


    #svgs2ttf(HASH): convert HASH to ttf file (HASH 안의 모든 svg -> ttf)
    logging.info("svgs2ttf start for userID: %s, count: %s" % (userID, count))
    ttf_converted = svgs2ttf(svg_set)

    #ttf2S3(userID, count, ttf, s3key_ttfs): save converted ttf file to S3 (완성된 ttf S3에 저장)
    logging.info("save ttf2S3 start for userID: %s, count: %s" % (userID,
                                                                  count))
    # ttf2S3(env, userID, count, ttf_converted)
    woff_addr = woff2S3(env, userID, count, ttf_converted)

    logging.info("-----END BACKPROCESSING for userID: %s, count: %s-----" %
                 (userID, count))
    logging.info("------------------------------------------------------------")
    return woff_addr


def test():
    test_userID = 'seo'
    test_count = 0
    test_unicodes = ["B9DD"]
    test_env = 'development'
    woff_addr = back_processing(test_userID, test_count, test_unicodes,
                                test_env)
    print(woff_addr)


if __name__ == '__main__':
    set_logging('test_log.txt')
    test()
