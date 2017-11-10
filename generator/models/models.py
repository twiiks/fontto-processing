from .test_model import TestModel

def create_model(opt, path_pth):
    model = TestModel()
    model.initialize(opt, path_pth)
    return model
