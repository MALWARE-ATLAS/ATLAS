#!/usr/bin/env python3

import argparse

try:
    from .lib.screen import printer
    from .lib.executor import executor
    from .lib.executor import executor_silent
    from .lib.linker_loader import linker
except:
    from lib.screen import printer
    from lib.executor import executor
    from lib.executor import executor_silent
    from lib.linker_loader import linker

# https://sumit-ghosh.com/articles/parsing-dictionary-key-value-pairs-kwargs-argparse-python/
class parse_params(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


class ATLAS:

    def __init__(self, file_name: str, param: dict={}, printer: object=None) -> None:
        self.file_name = file_name
        self.param = param
        self.printer = printer

        self.linked = linker(self.file_name, self.param)

    def execute(self) -> bool:
        result = False

        if self.linked != None:
            if self.printer != None:
                result = executor(self.linked, self.printer)
            else:
                result = executor_silent(self.linked)

        return result

    @property
    def chain(self: object) -> object:
        return self.linked.CHAIN


def main() -> bool:
    s_printer = printer()
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

    atlas = ATLAS(file_name, args.param, s_printer)
    atlas.execute()

    return True


if __name__ == "__main__":
    main()