import argparse
from omnidetector import *

if __name__ == "__main__":
    from fcl_options_icarus_geant4 import FCL_OPTIONS, BASE_FCL

    parser = argparse.ArgumentParser()
    parser.add_argument("--base-fcl", "-b", default=BASE_FCL, help="Base fhicl file to use.")
    add_fcl_options(parser, FCL_OPTIONS)

    args = parser.parse_args()
    validate_args(args)
    main(args, FCL_OPTIONS)

