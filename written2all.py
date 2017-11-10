import os
from generator.generator import generator
from utils import pil2tensor
import logging


def written2all(input_unicode, image_input, opt):
    path_class = "./data/pths/%s/" % (input_unicode)
    if not os.path.isdir(path_class):
        return {}

    output_images = {}

    # change image type to tensor float
    image_input_tensor = pil2tensor(image_input)
    image_input_tensor = image_input_tensor.unsqueeze(0)

    # if pth exist, generate another character using pth
    dirs = os.listdir(path_class)
    for dir in dirs:
        if dir.split('_')[0] == input_unicode:
            files = os.listdir("%s/%s/" % (path_class, dir))
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == '.pth':
                    unicode_output = dir.split('_')[1].split('.')[-1]
                    # log
                    logging.info("  start making:[ " + unicode_output + " ]")
                    path_pth = os.path.abspath("%s/%s/%s" % (path_class, dir,
                                                             filename))
                    logging.info("  done making!:[ " + unicode_output + " ]")
                    image_gen = generator(image_input_tensor, opt, path_pth)
                    output_images[unicode_output] = image_gen
                    break
    return output_images
