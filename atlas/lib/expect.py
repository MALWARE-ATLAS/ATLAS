def is_not_none(data: any) -> bool:
    return not data == None

def is_not_empty_list(data: list) -> bool:
    if type(data) is not list:
        return False
    
    return len(data)

def is_not_empty_dict(data: dict) -> bool:
    if type(data) is not dict:
        return False
    
    return len(data)

def is_not_empty_str(data: str) -> bool:
    if type(data) is not str:
        return False
    
    return data == ""

try:
    import magic

    def is_pe(data: bytes) -> bool:
        try:
            data_magic = magic.from_buffer(data, mime = True)
        except Exception as e:
            return False

        return data_magic == 'application/x-dosexec'
except:
    pass

def is_true(boolean: bool) -> bool:
    return True == boolean
