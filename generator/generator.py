from generator.models.models import create_model
import generator.util.util as util
from PIL import Image

# image_input_tensor should be tensor float
# one2class should call
#  image_input_tensor = to_tensor(image_input)
#  image_input_tensor = image_input_tensor.unsqueeze(0)
# return image is typed with PIL


def generator(image_input_tensor, opt, path_pth):
    # load model from path_pth
    model = create_model(opt, path_pth)
    model.set_input_GB(image_input_tensor)
    # test model
    model.test()
    # change to pil typed image
    fake_B = util.tensor2im(model.fake_B.data)
    image_generated_pil = Image.fromarray(fake_B, 'RGB')

    return image_generated_pil
