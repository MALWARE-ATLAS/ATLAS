# https://github.com/sulinx/remote_importer/blob/master/remote_importer.py
# http://wakandan.github.io/2018/06/07/python3-import-hook.html
# https://www.xorrior.com/In-Memory-Python-Imports/

import re
import sys
import types


MODULES = {}

class atl_importer():
    
    module_names = ""
    script = ""

    def __init__(self: object, *args) -> None:
        self.module_names = args
        self.path = None

    def find_module(self: object, fullname: str, path: str = None) -> object:
        global MODULES

        if re.search(r'^atl_.+?$', fullname) and \
           MODULES.get(fullname, '') != '':
            return self

        return None

    def load_module(self: object, name: str):
        global MODULES

        if name in sys.modules:
            return sys.modules[name]

        source = MODULES[name]
        code = compile(source, 'test', 'exec')
        mod = sys.modules.get(name)

        if mod is None:
            mod = sys.modules[name] = types.ModuleType(name)

        mod.__loader__ = self
        mod.__name__ = name
        exec(code, mod.__dict__)
        
        return mod

sys.meta_path.insert(-1, atl_importer())