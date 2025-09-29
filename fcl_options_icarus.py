import random

BASE_FCL = "detsim_2d_icarus_refactored_yzsim_notrigger.fcl"

OVERRIDE_PATH = "physics.producers.daq.wcls_main"

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

class Gain(FclOption):
    longopt = "--gain"
    shortopt = "-g"
    name = "Gain"
    default = 1
    rand_default = 0.1
    path = OVERRIDE_PATH + ".structs.gain"
    argtype = float

@register_fclopt
class Gain0(Gain):
    longopt = "--gain0"
    shortopt = "-g0"
    name = "Gain0"
    default = 18.0839
    path = OVERRIDE_PATH + ".structs.gain0"

@register_fclopt
class Gain1(Gain):
    longopt = "--gain1"
    shortopt = "-g1"
    name = "Gain1"
    default = 12.2379
    path = OVERRIDE_PATH + ".structs.gain1"

@register_fclopt
class Gain2(Gain):
    longopt = "--gain2"
    shortopt = "-g2"
    name = "Gain2"
    default = 13.8819
    path = OVERRIDE_PATH + ".structs.gain2"

class Shaping(FclOption):
    longopt = "--shaping"
    shortopt = "-s"
    name = "Shaping Time"
    default = 1.3
    rand_default = 0.05
    path = OVERRIDE_PATH + ".structs.shaping"
    argtype = float

@register_fclopt
class Shaping0(Shaping):
    longopt = "--shaping0"
    shortopt = "-s0"
    name = "Shaping Time P0"
    path = OVERRIDE_PATH + ".structs.shaping0"

@register_fclopt
class Shaping1(Shaping):
    longopt = "--shaping1"
    shortopt = "-s1"
    name = "Shaping Time P1"
    default = 1.45 # different on middle induction
    path = OVERRIDE_PATH + ".structs.shaping1"

@register_fclopt
class Shaping2(Shaping):
    longopt = "--shaping2"
    shortopt = "-s2"
    name = "Shaping Time P2"
    path = OVERRIDE_PATH + ".structs.shaping2"

@register_fclopt
class CohNoise(FclOption):
    longopt = "--coh-noise"
    shortopt = "-cn"
    name = "Coherent Noise"
    default = 1
    rand_default = 0.05
    path = OVERRIDE_PATH + ".structs.coh_noise_scale"
    argtype = float

@register_fclopt
class IntNoise(FclOption):
    longopt = "--int-noise"
    shortopt = "-in"
    name = "Inherent Noise"
    default = 1
    rand_default = 0.05
    path = OVERRIDE_PATH + ".structs.int_noise_scale"
    argtype = float

@register_fclopt
class Lifetime(FclOption):
    longopt = "--lifetime"
    shortopt = "-l"
    name = "Electron Lifetime"
    default = 3e3
    rand_default = 4e3
    path = OVERRIDE_PATH + ".structs.lifetime"
    argtype = float

    def draw(self, rand): # override to uniform
        return max(1e3, random.uniform(self.value - rand, self.value + rand))

@register_fclopt
class SignalShape(FclOption):
    longopt = "--signal-shape-index"
    shortopt = "-si"
    name = "Middle Induction Signal Shape Index"
    default = 7
    rand_default = 7
    path = OVERRIDE_PATH + ".params.files_fields"
    argtype = int

    def draw(self, rand): # override to uniform integer, clamp 0-14 inclusive
        return min(14, max(0, random.uniform(self.value - rand, self.value + rand)))

    def config(self):
        return self.path + ": " + ('"icarus_fnal_fit_ks_P0nom_P1bin%i.json.bz2"' % self.value)

