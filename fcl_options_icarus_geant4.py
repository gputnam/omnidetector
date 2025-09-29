import random
from fcl_options import *

BASE_FCL = "larg4_icarus_cosmics_sce.fcl"

OVERRIDE_PATH = "services.LArG4Parameters"

@register_fclopt
class EMBA(FclOption):
    longopt = "--alpha"
    shortopt = "-a"
    name = "EMB alpha"
    default = 0.904
    rand_default = 0.01
    path = OVERRIDE_PATH + ".EllipsModBoxA"
    argtype = float

@register_fclopt
class EMBB(FclOption):
    longopt = "--beta"
    shortopt = "-b"
    name = "EMB beta"
    default = 0.204
    rand_default = 0.04
    path = OVERRIDE_PATH + ".EllipsModBoxB"
    argtype = float

@register_fclopt
class EMBR(FclOption):
    longopt = "--R"
    shortopt = "-R"
    name = "EMB R"
    default = 1.25
    rand_default = 0.02
    path = OVERRIDE_PATH + ".EllipsModBoxR"
    argtype = float
