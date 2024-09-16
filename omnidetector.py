import argparse
from fcl_options_icarus import FCL_OPTIONS, BASE_FCL

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

def main(args):
    fcl_out = fhicl_template.format(
        base_fcl=args.base_fcl,
        overrides="\n".join([build_opt(opt, args).config() for opt in FCL_OPTIONS if has_opt(opt, args)])
    )

    print(fcl_out)

def validate_args(args):
    pass

def add_fcl_options(parser):
    for opt in FCL_OPTIONS:
        parser.add_argument("%s-set" % opt.longopt, "%ss" % opt.shortopt, 
            help="Set %s central value. Default is %s." % (opt.name, str(opt.default)), 
            required=False, type=opt.argtype, default=None)
        parser.add_argument("%s-rand" % opt.longopt, "%sr" % opt.shortopt, 
            help="Draw %s from distribution. Optional: set distribution width. Default is %s." % (opt.name, str(opt.rand_default)), 
            nargs="?", default=None, const=opt.rand_default, type=opt.argtype)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-fcl", "-b", default=BASE_FCL, help="Base fhicl file to use.")
    add_fcl_options(parser)

    args = parser.parse_args()
    validate_args(args)
    main(args)

