import random
from fcl_options import *

BASE_FCL = "detsim_2d_icarus_refactored_yzsim_notrigger.fcl"

OVERRIDE_PATH = "physics.producers.daq.wcls_main"

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
class Attenuation(FclOption):
    longopt = "--attenuation"
    shortopt = "-a"
    name = "Electron Attenuation"
    default = 0.2
    rand_default = 0.1
    path = OVERRIDE_PATH + ".structs.lifetime"
    argtype = float

    def draw(self, rand): # override to uniform
        return max(0.01, random.uniform(self.value - rand, self.value + rand))*1e-3

    def config(self):
        return self.path + ": " + str(1/self.value)

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

class ShapeGain(FclOption):
    longopt = "--shape-gain"
    shortopt = "-sg"
    name = "Signal Shape + Gain"

    argtype = lambda s: None if s is None else (float(s.split(",")[0]), float(s.split(",")[1]))
    default = (1.3, 1)
    rand_default = (0.2, 0.05)
    path = (OVERRIDE_PATH + ".structs.shaping", OVERRIDE_PATH + ".structs.gain")

    def draw(self, rand):
        return self.value[0]*random.uniform(1 - rand[0], 1 + rand[0]), self.value[1]*(1 + random.gauss(0., sigma=rand[1]))

    def config(self):
        values = (self.value[0], self.value[1]*(self.default[0]/self.value[0])) # scale gain to shaping
        return "\n".join([p + ": " + str(v) for (p, v) in zip(self.path, values)])

@register_fclopt
class ShapeGain0(ShapeGain):
    longopt = "--shapegain0"
    shortopt = "-sg0"
    name = "Shaping Time + Gain P0"
    path = (OVERRIDE_PATH + ".structs.shaping0", OVERRIDE_PATH + ".structs.gain0")

@register_fclopt
class ShapeGain1(ShapeGain):
    longopt = "--shapegain1"
    shortopt = "-sg1"
    name = "Shaping Time + Gain P1"
    default = (1.45, 1) # different on middle induction
    path = (OVERRIDE_PATH + ".structs.shaping1", OVERRIDE_PATH + ".structs.gain1")

@register_fclopt
class ShapeGain2(ShapeGain):
    longopt = "--shapegain2"
    shortopt = "-sg2"
    name = "Shaping Time + Gain P2"
    path = (OVERRIDE_PATH + ".structs.shaping2", OVERRIDE_PATH + ".structs.gain2")


