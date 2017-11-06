#!/usr/bin/python3
# -*- coding: utf-8 -*-
from written2all import written2all
from utils import url2img, store2S3, ttf2S3
from modify import trim_resize_PIL, noise_filter, vectoralize, svgs2ttf

#received_message -> processing -> output
def backProcessing(userID, count, unicodes, env):
    print("START BACKPROCESSING for userID: %s, count: %s\n" %(userID, count))
    #INITIALIZE HASH: {'unicode': 'PIL_imgs'} (TTF 변환을 위한 hash)
    svg_set = {}
    
    #FOR each unicode IN unicodes (입력받은 각각의 글자에 대해 아래 작업 수행)
    for input_unicode in unicodes:
        print("START WITH SINGLE INPUT_UNICODE %s" %input_unicode)
        #get img_url from S3 WITH userID, count, unicode (입력값을 통해 S3에 있는 글자 주소 선언)
        s3key_input = '%s/inputs/%s/%s/%s' %(env, userID, count, input_unicode)
        input_address = 'https://s3.ap-northeast-2.amazonaws.com/fontto/' + s3key_input
        
        print("-----url2img start-----")
        #url2img(url): url_img -> PIL_img 
        input_PIL = url2img(input_address)


        print("-----trim_resize_PIL start-----")
        #trim_resize_PIL(PIL, width, height, border): trim PIL_img
        modified_PIL = trim_resize_PIL(input_PIL, 216, 216, 20)

        #store2S3(userID, count, input_unicode, user PIL_img, env, s3key_output_bitmap): save output BITMAPS of input image
        s3key_output_bitmap = '%s/outputs/bitmaps/%s/%s/%s' %(env, userID, count, input_unicode)
        print("-----save input bitmap PIL on S3 start-----")
        store2S3(userID, count, input_unicode, modified_PIL, env, s3key_output_bitmap)

        #vectoralize(user PIL_img): vectoralize user img
        print("-----vectoralize input PIL start-----")
        vectored_PIL = vectoralize(modified_PIL)
        #APPEND vectoralized user img to HASH
        svg_set[input_unicode] = vectored_PIL

        #store2S3(userID, count, input_unicode, vectored_PIL, env, s3key_vectors): save vectoralized image to vectors-S3
        s3key_output_vector = '%s/outputs/vectors/%s/%s/%s' %(env, userID, count, input_unicode)
        print("-----save vectoralized input PIL on S3 start")
        store2S3(userID, count, input_unicode, vectored_PIL, env, s3key_output_vector)


        #written2all(unicode, PIL_img): single PIL_img to multi PIL_imgs
        print("-----written2all start-----")
        output_images = written2all(input_unicode, modified_PIL)
        print("     SAME CLASS WITH unicode: %s are %s" %(input_unicode, output_images))

        
        #FOR each PIL_img IN PIL_imgs
        for output_unicode, output_image in output_images.items():
            #store2S3(userID, count, output_unicode, output_PIL, env, s3key_vectors): save PIL_imgs to S3
            s3key_output_bitmap = '%s/outputs/bitmaps/%s/%s/%s' %(env, userID, count, output_unicode)
            print("-----save output bitmap PIL on S3 start-----")
            store2S3(userID, count, output_unicode, output_image, env, s3key_output_bitmap)

            #noise_filter(PIL_img): noise reduction
            print("-----reducting output noise start-----")
            filterd = noise_filter(output_image)

            #vectoralize(PIL_img): vectoralize PIL_img
            print("-----vectoralize output PIL start-----")
            vectoralized = vectoralize(filterd)
            #APPEND vectoralized PIL_img to HASH
            svg_set[output_unicode] = vectoralized

            #store2S3(userID, count, output_unicode, vectored_PIL, env, s3key_vectors): save vectoralized image to vectors-S3
            s3key_output_vector = '%s/outputs/vectors/%s/%s/%s' %(env, userID, count, output_unicode)
            print("-----save vectoralized output PIL on S3 start-----")
            store2S3(userID, count, output_unicode, output_image, env, s3key_output_vector)

        print("END WITH SINGLE INPUT_UNICODE")
            

    #svgs2ttf(HASH): convert HASH to ttf file (HASH 안의 모든 svg -> ttf)
    print("\n-----svgs2ttf start-----")
    ttf_converted = svgs2ttf(svg_set)

    #ttf2S3(userID, count, ttf, s3key_ttfs): save converted ttf file to S3 (완성된 ttf S3에 저장)
    print("-----save ttf2S3 start-----")
    ttf2S3(userID, count, ttf_converted, env)

    print("END BACKPROCESSING for userID: %s, count: %s" %(userID, count))


