import random

FCL_OPTIONS = []

def register_fclopt(opt):
    FCL_OPTIONS.append(opt)
    return opt

class FclOption(object):
    # override these 
    longopt = None
    shortopt = None
    name = None
    default = None
    rand_default = None
    path = None 
    argtype = None

    def __init__(self, setv=None, rand=None):
        if setv is not None:
            self.value = setv
        else:
            self.value = self.default

        if rand is not None:
            self.value = self.draw(rand)

    def draw(self, rand):
        return self.value*(1 + random.gauss(0., sigma=rand))

    def config(self):
        return self.path + ": " + str(self.value)
