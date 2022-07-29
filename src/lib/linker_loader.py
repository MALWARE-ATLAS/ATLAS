import re
import os
import yaml
import base64

from glob import glob
from pprint import pprint
from collections import OrderedDict

from . import core, expect, error


LEXICON = {
    'headers': [
        'meta',
        'modules',
        'scripts',
        'chain'
    ],
    'words': [
        'input',
        'func',
        'output',
        'expect',
        'run'
    ]
}

ATL = {}
META = {}
CHAIN = []
MODULES = {}
MODULE_NAMES = set()
SCRIPTS = {}

SUBCHAIN_KEYS = []

class node:

    input = None
    func = None
    func_str = ""
    expect = None
    expect_str = []
    output = None
    output_str = ""

    def __init__(self: object, input: list, func: str, expect: str = "", output: str = "") -> None:
        self.input = input
        self.func_str = func
        self.expect_str = expect
        self.output_str = output
        self.expect = []


class linker:

    file_name = ""
    base_name = ""
    atl_yaml = yaml
    META = {}
    CHAIN = []
    MODULES = {}
    SCRIPTS = {}

    def __init__(self:object, file_name: str, param: dict={}) -> None:
        global ATL
        self.file_name = file_name
        self.param = param

        temp_file_name, file_extension = os.path.splitext(self.file_name)
        self.base_name = os.path.basename(temp_file_name)

        self.atl_yaml = self.link(self.file_name)
        
        if self.atl_yaml != None:
            temp = ATL
            ATL = {}
            ATL[self.base_name] = temp
            ATL[self.base_name] = {}
            ATL[self.base_name]['chain'] = self.CHAIN
            ATL[self.base_name]['scripts'] = self.SCRIPTS

            for i in self.MODULES:
                ATL[self.base_name][i] = self.MODULES[i]
            
            self.loader()

            


    def link(self: object, file_name: str) -> yaml:
        result = None
        atl = ""
        atl_loaded = None

        if not os.path.isfile(file_name):
            return result
        
        with open(file_name, 'r') as file:
            atl = file.read()

        try:
            atl_loaded = yaml.load(atl, Loader=yaml.Loader)
        except Exception as e:
            print(e)
            return result

        if len(atl_loaded.get('chain', [])) > 0 and self.lexical_analysis(atl_loaded):
            result = atl_loaded

        return result

    def lexical_analysis(self: object, atl: list) -> bool:
        result = False
        is_chain = False
        
        for i in atl:
            if i not in LEXICON['headers']:
                return result
            if i == 'chain':
                is_chain = True

        if not is_chain:
            return result

        if not self.lexical_analysis_meta(atl.get('meta', [])) or \
           not self.lexical_analysis_scripts(atl.get('scripts', [])) or \
           not self.lexical_analysis_modules(atl.get('modules', [])) or \
           not self.lexical_analysis_chain(atl['chain']):
            return result
        
        result = True

        return result


    def lexical_analysis_chain(self: object, chain: list) -> bool:
        global SUBCHAIN_KEYS

        result = False
        temp = OrderedDict()
        input = []
        func = ""
        expect = []
        output = ""
        sub_input = []
        sub_func = ""
        sub_expect = []
        sub_output = ""
        sub_chain = []

        for i in chain:
            sub_chain = chain[i]
            input = []
            func = ""
            expect = []
            output = ""
            
            if i in SUBCHAIN_KEYS:
                raise(error.DuplicateKeyUsage(i))
            elif i in LEXICON['headers'] or \
                 i in LEXICON['words']:
                raise(error.SpecialKeyUsage(i))
            
            SUBCHAIN_KEYS.append(i)

            if type(chain[i]) is str and \
               chain[i][0] == '$' and \
               '.' in chain[i]:
                keys = chain[i][1:].split('.')
                value = self.MODULES
                
                try:
                    for j in keys:
                        value = value[j]
                    
                    if type(value) is OrderedDict and \
                       keys[1] == 'chain':
                        for j in value:
                            temp[j] = value[j]
                    else:
                        temp[i] = value
                except Exception as e:
                    print(e)
                    return result

            elif type(sub_chain) is dict:
                for j in sub_chain:
                    keys = []
                    value = ""

                    if j == 'input':
                        if type(sub_chain[j]) is str:
                            input.append(sub_chain[j])
                        elif type(sub_chain[j]) is list:
                            input += sub_chain[j]
                        else:
                            return result
                    elif j == 'func':
                        func = sub_chain[j]
                    elif j == 'expect':
                        if type(sub_chain[j]) is str:
                            expect.append(sub_chain[j])
                        elif type(sub_chain[j]) is list:
                            expect += sub_chain[j]
                        else:
                            return result
                    elif j == 'output':
                        output = sub_chain[j]
                    elif type(sub_chain[j]) is dict:
                        sub_input = []
                        sub_func = ""
                        sub_expect = []
                        sub_output = ""

                        if j in SUBCHAIN_KEYS:
                            raise(error.DuplicateKeyUsage(j))
                        elif j in LEXICON['headers'] or \
                             j in LEXICON['words']:
                            raise(error.DuplicateKeyUsage(j))
                        
                        SUBCHAIN_KEYS.append(j)

                        for k in sub_chain[j]:

                            if k == 'input':
                                if type(sub_chain[j][k]) is str:
                                    sub_input.append(sub_chain[j][k])
                                elif type(sub_chain[j][k]) is list:
                                    sub_input += sub_chain[j][k]
                                else:
                                    return result
                            elif k == 'func':
                                sub_func = sub_chain[j][k]
                            elif k == 'expect':
                                if type(sub_chain[j][k]) is str:
                                    sub_expect.append(sub_chain[j][k])
                                elif type(sub_chain[j][k]) is list:
                                    sub_expect += sub_chain[j][k]
                                else:
                                    return result
                            elif k == 'output':
                                sub_output = sub_chain[j][k]
                            else:
                                return result

                        # if (not len(sub_input) > 0 and not len(input)) or \
                        if sub_func == "" or \
                           (sub_expect == [] and expect == []):
                            return result
                        
                        if temp.get(i, {}) == {}:
                            temp[i] = OrderedDict()

                        if sub_expect == [] and \
                           expect != []:
                            sub_expect = expect
                        temp[i][j] = node(input + sub_input, sub_func, sub_expect, sub_output)

                        continue
                    else:
                        return result
                
                if func == "" and sub_func == "":
                    return result

                if temp.get(i, []) == []:
                    temp[i] = node(input, func, expect, output)
            else:
                return result

        result = True
        self.CHAIN = temp

        return result
        

    def lexical_analysis_scripts(self: object, scripts: list) -> bool:
        result = False
        
        if scripts == []:
            result = True
        else:
            for i in scripts:
                pre_result = False

                if type(i) is not str or type(scripts[i]) is not str:
                    return result
                elif i == 'run':
                    raise(error.RunKeyUsage)
                try:
                    script_bytes = bytes(scripts[i], 'ascii')

                    if base64.b64encode(base64.b64decode(script_bytes)) != script_bytes:
                        return result
                except Exception as e:
                    print(e)
                    return result

            result = True

        self.SCRIPTS = scripts

        return result


    def lexical_analysis_meta(self: object, meta: list) -> bool:
        result = False
        
        if meta == []:
            result = True
        else:
            for i in meta:
                if type(i) is not str or type(meta[i]) is not str:
                    return result

            result = True

        self.META = meta

        return result


    def lexical_analysis_modules(self: object, modules: list) -> bool:
        result = False
        
        if modules == []:
            result = True
        else:
            for i in modules:
                if type(i) is not str:
                    return result

            if not self.module_check(modules):
                return result

            result = True

        return result


    def module_check(self: object, modules: list) -> bool:
        result = False
        module_paths = []
        global MODULES
        global MODULE_NAMES

        if modules == []:
            result = True
        else:
            for i in modules:
                temp = []
                file_name = ""
                file_extension = ""

                try:
                    file_name, file_extension = os.path.splitext(i)
                except Exception as e:
                    print(e)
                    return result
                
                if file_extension == '':
                    i = i + '.atl'

                if '*' in i:
                    try:
                        temp = glob.glob(i)
                    except Exception as e:
                        print(e)
                        return result
                else:
                    temp.append(i)
                
                for j in temp:
                    module_linked = None
                    base_name = ""
                    if file_name not in MODULE_NAMES:
                        try:
                            module_linked = linker(j)
                            if module_linked == None:
                                return result

                            base_name = os.path.basename(file_name)
                            self.MODULES[base_name] = {}
                            self.MODULES[base_name]['chain'] = module_linked.CHAIN
                            self.MODULES[base_name]['scripts'] = module_linked.SCRIPTS
                            MODULE_NAMES.add(file_name)
                        except Exception as e:
                            print(e)
                            return result

        result = True

        return result


    def loader(self: object) -> bool:
        result = False
        global ATL
        global SUBCHAIN_KEYS

        for i in self.CHAIN:
            if type(self.CHAIN[i]) == OrderedDict:
                for j in self.CHAIN[i]:
                    try:
                        self.CHAIN[i][j].func = getattr(core, self.CHAIN[i][j].func_str)

                        if self.CHAIN[i][j].expect_str != []:
                            for k in self.CHAIN[i][j].expect_str:
                                self.CHAIN[i][j].expect.append(getattr(expect, k))
                    except Exception as e:
                        print(e)
                        return result
                    
                    for k in range(0, len(self.CHAIN[i][j].input)):
                        if self.CHAIN[i][j].input[k][0] == '$':
                            keys = self.CHAIN[i][j].input[k][1:].split('.')
                            if keys[0] == 'param':
                                try:
                                    self.CHAIN[i][j].input[k] = self.param[keys[1]]
                                except:
                                    raise(error.ParamKeyMissing(keys[1]))
                            else:
                                value = ATL[self.base_name]

                                try:
                                    for z in keys:
                                        value = value[z]
                                    
                                    if re.search(r'^.*scripts\.[a-zA-Z0-9_]+$', self.CHAIN[i][j].input[k][1:]):
                                        self.CHAIN[i][j].input[k] = (value, keys[len(keys) - 1])
                                    else:
                                        self.CHAIN[i][j].input[k] = value
                                except Exception as e:
                                    if z not in SUBCHAIN_KEYS:
                                        return result
                                    continue
                            

            else:
                try:
                    self.CHAIN[i].func = getattr(core, self.CHAIN[i].func_str)

                    if self.CHAIN[i].expect_str != []:
                        for j in self.CHAIN[i].expect_str:
                            self.CHAIN[i].expect.append(getattr(expect, j))
                except Exception as e:
                    print(e)
                    return result

                for j in range(0, len(self.CHAIN[i].input)):
                    if self.CHAIN[i].input[j][0] == '$':
                        keys = self.CHAIN[i].input[j][1:].split('.')
                        if keys[0] == 'param':
                            try:
                                self.CHAIN[i].input[j] = self.param[keys[1]]
                            except:
                                raise(error.ParamKeyMissing(keys[1]))
                        else:
                            value = ATL[self.base_name]

                            try:
                                for z in keys:
                                    value = value[z]
                                if re.search(r'^.*scripts\.[a-zA-Z0-9_]+$', self.CHAIN[i].input[j][1:]):
                                    self.CHAIN[i].input[j] = (value, keys[len(keys) - 1])
                                else:
                                    self.CHAIN[i].input[j] = value
                            except Exception as e:
                                if z not in SUBCHAIN_KEYS:
                                    return result
                                continue
        result = True

        return result