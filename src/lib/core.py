import re
import sys
import base64
import hashlib
import platform
import requests

from subprocess import Popen, TimeoutExpired, PIPE

from typing import Dict, List

from . import atl_importer

POWERSHELL_DICT = {
                'Linux': 'pwsh',
                'Darwin': 'pwsh',
                'Java': None,
                'Windows': 'powershell.exe'
}

POWERSHELL_NAME = ""

try:
    plat = platform.system()
    POWERSHELL_NAME = POWERSHELL_DICT[plat]
except Exception as e:
    print(e)


def reverse(data: any) -> any:
    return data[::-1]

def download_from_remote_server(addr: str) -> bytes:
    result = b''

    try:
        response = requests.get(url=addr)
        result = response.content
    except Exception as e:
        sys.stderr.write(str(e))
        
    return result


def powershell_executor(script_name: tuple, *args) -> any:
    global POWERSHELL_NAME
    result = None
    script, name = script_name
    args_list = []

    with Popen([POWERSHELL_NAME, "-Command", r"-"], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=8192, universal_newlines=True) as proc:

        for i in range(int(len(script) / 10000) + 1):
            proc.stdin.write('$script=$script+"{}"\r\n'.format(script[i * 10000:(i + 1) * 10000]))
            proc.stdin.flush()

        proc.stdin.write('\
                $decoded_script=[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($script));\
                $ScriptBlock=[ScriptBlock]::Create($decoded_script);\
                . $ScriptBlock;\r\n\
            ')
        proc.stdin.flush()
        
        for i in range(len(args)):
            temp = ""
            if type(args[i]) is str:
                temp = args[i]
                for j in range(0, int(len(temp) / 10000) + 1):
                    proc.stdin.write('$arg{}=$arg{}+"{}";\r\n'.format(i + 1, i + 1, temp[j * 10000:(j + 1) * 10000]))
                    proc.stdin.flush()
                    #print('$arg{}=$arg{}+"{}"\r\n'.format(i + 1, i + 1, temp[j * 10000:(j + 1) * 10000]))
            elif type(args[i]) is bytes:
                temp = base64.b64encode(args[i]).decode()
                for j in range(0, int(len(temp) / 10000) + 1):
                    proc.stdin.write('$encoded_arg{}=$encoded_arg{}+"{}";\r\n'.format(i + 1, i + 1, temp[j * 10000:(j + 1) * 10000]))
                    proc.stdin.flush()
                
                proc.stdin.write('$arg{}=([System.Convert]::FromBase64String($encoded_arg{}));'.format(i + 1, i + 1))
                proc.stdin.flush()

            args_list.append("$arg{}".format(i + 1))
        proc.stdin.write('\
                try {{\
                    $result={0} {1};\
                }}\
                catch {{\
                    $result=run {1};\
                }}\
                $result_encoded=[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($result));\
                $temp_file=New-TemporaryFile;\
                $return_file_path=Join-Path -Path $temp_file.DirectoryName -ChildPath $temp_file.Name;\
                Set-Content $return_file_path -Value $result_encoded -Encoding Ascii;\
                $return_file_path\r\n\
            '.format(name, " ".join(args_list)))

        # Because the PIPE's buffer filled up with data bigger than 64k, can't get the stdout directly.
        # Then decided to get it via tempfile.
        output, _ = proc.communicate()
        try:
            if proc.poll() != None:
                proc.kill()
            output = re.sub('(\n)|(\r)|(\\x1b\[\?1(h|l))', '', output)
            result = base64.b64decode(file_read_bin(output))
        except TimeoutExpired:
            proc.kill()
        except Exception as e:
            proc.kill()
            sys.stderr.write(str(e))
            return result
    
    return result

def file_read_bin(path: str) -> bytes:
    result = b''

    try:
        with open(path, 'rb') as file:
            result = file.read()
    except Exception as e:
        sys.stderr.write(str(e))

    return result

def file_read_utf8(path: str) -> str:
    result = ''

    try:
        with open(path, 'r') as file:
            result = file.read()
    except Exception as e:
        sys.stderr.write(str(e))

    return result
    

def save_file_bytes(data: any, prefix: str = '') -> bool:
    result = False
    sha256 = get_sha256(data)

    try:
        with open("{}{}.bin".format(prefix, sha256), 'wb') as file:
            if type(data) is bytes:
                file.write(data)
            elif type(data) is str:
                file.write(data.encode())
            else:
                return result
    except Exception as e:
        sys.stderr.write(str(e))
        return result
    
    result = True

    return result


def save_file_arr(arr: list, prefix: str = 'output') -> bool:
    result = False

    try:
        for i in range(0, len(arr)):
            with open("{}_{}".format(prefix, i), 'wb') as file:
                if type(arr[i]) is bytes:
                    file.write(arr[i])
                elif type(arr[i]) is str:
                    file.write(arr[i].encode())
                else:
                    return result
    except Exception as e:
        sys.stderr.write(str(e))
        return result
    
    result = True

    return result


def python_executor(script_tuple: tuple, *args) -> any:
    result = None
    decoded_script = ""
    script, script_name = script_tuple
    name = 'atl_' + script_name

    try:
        decoded_script = base64.b64decode(script)
        
        if atl_importer.MODULES.get(name, '') == '':
            atl_importer.MODULES[name] = decoded_script
            imported = __import__(name)
        else:
            imported = sys.modules[name]

        try:
            func = getattr(imported, script_name)
        except AttributeError:
            func = getattr(imported, 'run')

        result = func(*args)
    except Exception as e:
        sys.stderr.write(str(e))

    return result


def printer(*args) -> bool:

    print(" ".join(args))
    return True


def hello_world() -> None:
    print("Hello World, ATLAS.")

    return True

def get_sha256(data: bytes) -> str:
    sha256 = ''
    
    try:
        sha256 = hashlib.sha256(bytearray(data)).hexdigest()
    except Exception as e:
        sys.stderr.write(str(e))

    return sha256

def bytes_to_str_utf8(data: bytes=b'') -> str:
    try:
        return data.decode('utf8')
    except Exception as e:
        sys.stderr.write(str(e))
        return ''

    