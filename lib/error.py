class UndefinedFuncValue(Exception):
    def __init__(self, func: str):
        super().__init__(f'{func} is missing in the core library.')


class UndefinedExpectValue(Exception):
    def __init__(self, expect: str):
        super().__init__(f'{expect} is missing in the expect library.')


class ParamKeyMissing(Exception):
    def __init__(self, key: str):
        super().__init__(f'{key} is missing in command-line argument param.')


class SpecialKeyUsage(Exception):
    def __init__(self, key: str):
        super().__init__(f'{key}')


class DuplicateKeyUsage(Exception):
    def __init__(self, key: str):
        super().__init__(f'{key}')


class RunKeyUsage(Exception):
    def __init__(self):
        super().__init__()


class ChainSectionMissing(Exception):
    def __init__(self):
        super().__init__(f'The rule doesn\'t have chain section.')


class ChainSectionEmpty(Exception):
    def __init__(self):
        super().__init__(f'The rule\'s chain section is empty.')


class FuncMissing(Exception):
    def __init__(self, subchain: str):
        super().__init__(f'The {subchain} must have func key')


class ExpectMissing(Exception):
    def __init__(self, subchain: str):
        super().__init__(f'The {subchain} must have expect key')


class ScriptsBase64ValueError(Exception):
    def __init__(self, script: str):
        super().__init__(f'The {script}\'s value raise an Base64 exception.')


