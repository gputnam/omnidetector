import argparse

fhicl_template = \
"""#include "{base_fcl}"
{overrides}"""

def build_opt(opt, args):
    rnd = getattr(args, ("%s_rand" % opt.longopt)[2:].replace("-", "_"))
    set = getattr(args, ("%s_set" % opt.longopt)[2:].replace("-", "_"))
    return opt(set, rnd)

def has_opt(opt, args):
    rnd = getattr(args, ("%s_rand" % opt.longopt)[2:].replace("-", "_"))
    set = getattr(args, ("%s_set" % opt.longopt)[2:].replace("-", "_"))
    return (rnd is not None) or (set is not None)

def main(args, options):
    fcl_out = fhicl_template.format(
        base_fcl=args.base_fcl,
        overrides="\n".join([build_opt(opt, args).config() for opt in options if has_opt(opt, args)])
    )

    print(fcl_out)

def validate_args(args):
    pass

def add_fcl_options(parser, options):
    for opt in options:
        parser.add_argument("%s-set" % opt.longopt, "%ss" % opt.shortopt, 
            help="Set %s central value. Default is %s." % (opt.name, str(opt.default)), 
            required=False, type=opt.argtype, default=None)
        parser.add_argument("%s-rand" % opt.longopt, "%sr" % opt.shortopt, 
            help="Draw %s from distribution. Optional: set distribution width. Default is %s." % (opt.name, str(opt.rand_default)), 
            nargs="?", default=None, const=opt.rand_default, type=opt.argtype)
