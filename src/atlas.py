#!/usr/bin/env python3

import argparse
import platform

try:
    from .lib.screen import printer
    from .lib.executor import executor 
    from .lib.linker_loader import linker
except:
    from lib.screen import printer
    from lib.executor import executor 
    from lib.linker_loader import linker

# https://sumit-ghosh.com/articles/parsing-dictionary-key-value-pairs-kwargs-argparse-python/
class parse_params(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value



def main() -> bool:
    plat = platform.system()
    s_printer = printer(plat)

    epilog = """Example Usage:

  atlas -a HelloWorld.atl
  atlas -a some.atl --param foo=bar
    """
    argumentParser = argparse.ArgumentParser(
        "ATLAS",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    argumentParser.add_argument(
        '-a', '--atl-file',
        nargs=1,
        required=True,
        help='ATLAS rule file'
    )
    argumentParser.add_argument(
        '-p', '--param',
        nargs='*',
        required=False,
        help='Parameters to use inside the rule, key=value',
        action=parse_params
    )
    args = argumentParser.parse_args()
    
    file_name = args.atl_file[0]

    linked = linker(file_name, args.param)
    
    if linked != None:
        executor(linked, s_printer)

    return True


if __name__ == "__main__":
    main()