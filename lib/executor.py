import time
import threading
import json
import io

from typing import Dict, List, final
from contextlib import redirect_stdout, redirect_stderr
from collections import OrderedDict


def node_to_dict(node: object, stdout: str, stderr: str) -> Dict:
    result = {
        'func': '',
        'input': [],
        'expect': [],
        'output': None
    }

    try:
        result['func'] = node.func_str
        result['expect'] = node.expect_str
        
        for i in node.input:
            if type(i) == str:
                result['input'].append(i[:50])
            elif type(i) == int:
                result['input'].append(int(str(i)[:50]))
            elif type(i) == bytes:
                result['input'].append(str(i[:50]))
            elif type(i) == bool:
                result['input'].append(i)
            else:
                result['input'].append(str(type(i)))

        if type(node.output) == str:
            result['output'] = node.output[:50]
        elif type(node.output) == int:
            result['output'] = int(str(node.output)[:50])
        elif type(node.output) == bytes:
            result['output'] = str(node.output[:50])
        elif type(node.output) == bool:
            result['output'] = node.output
        else:
            result['output'] = str(type(node.output))
        

        result['stdout'] = stdout[:200]
        result['stderr'] = stderr[:200]
    except Exception as e:
        print(e)
    
    return result



def executor(linked: object, s_printer: object) -> bool:
    result = False

    for i in linked.CHAIN:
        res = None
        if type(linked.CHAIN[i]) is OrderedDict:
            print('\033[4m' + '\033[1m' + f'[+] {i}' + '\033[0m')
            for j in linked.CHAIN[i]:
                res = None
                positive = False

                thread1 = threading.Thread(
                    target=s_printer.status,
                    args=(j, 1,),
                    daemon=True)
                thread1.start()

                for k in range(0, len(linked.CHAIN[i][j].input)):
                    if linked.CHAIN[i][j].input[k][0] == '$':
                        keys = linked.CHAIN[i][j].input[k][1:].split('.')
                        temp = linked.CHAIN

                        try:
                            for z in keys:
                                temp = temp[z]
                            linked.CHAIN[i][j].input[k] = temp.output
                        except Exception as e:
                            print(e)
                            return result
                

                with redirect_stdout(io.StringIO()) as stdout, \
                     redirect_stderr(io.StringIO()) as stderr:
                    res = linked.CHAIN[i][j].func(*linked.CHAIN[i][j].input)

                if linked.CHAIN[i][j].expect != []:
                    for k in range(len(linked.CHAIN[i][j].expect)):
                        if not linked.CHAIN[i][j].expect[k](res):
                            s_printer.return_code = 99
                            thread1.join()
                            node_dict = node_to_dict(linked.CHAIN[i][j], stdout.getvalue(), stderr.getvalue())
                            print(json.dumps(node_dict, indent=8))
                            print()
                            break
                        elif k == len(linked.CHAIN[i][j].expect) - 1:
                            positive = True

                            s_printer.return_code = 99
                            thread1.join()
                            node_dict = node_to_dict(linked.CHAIN[i][j], stdout.getvalue(), stderr.getvalue())
                            print(json.dumps(node_dict, indent=8))
                            print()
                            
                            linked.CHAIN[i][j].output = res
                            linked.CHAIN[i] = linked.CHAIN[i][j]
                    if positive:
                        break
                elif res == True:
                    positive = True
                    linked.CHAIN[i] = linked.CHAIN[i][j]
                    
                    s_printer.return_code = 99
                    thread1.join()
                    node_dict = node_to_dict(linked.CHAIN[i][j], stdout.getvalue(), stderr.getvalue())
                    print(json.dumps(node_dict, indent=8))
                    print()

                    break
            
            if not positive:
                return result
        else:
            thread1 = threading.Thread(
                target=s_printer.status,
                args=(i,),
                daemon=True)
            thread1.start()
            for k in range(0, len(linked.CHAIN[i].input)):
                if linked.CHAIN[i].input[k][0] == '$':
                    keys = linked.CHAIN[i].input[k][1:].split('.')
                    temp = linked.CHAIN

                    try:
                        for z in keys:
                            temp = temp[z]
                        linked.CHAIN[i].input[k] = temp.output
                    except Exception as e:
                        print(e)
                        return result


            with redirect_stdout(io.StringIO()) as stdout, \
                 redirect_stderr(io.StringIO()) as stderr:
                res = linked.CHAIN[i].func(*linked.CHAIN[i].input)

            if linked.CHAIN[i].expect != []:
                for j in range(len(linked.CHAIN[i].expect)):
                    if not linked.CHAIN[i].expect[j](res):
                        return result
                    elif j == len(linked.CHAIN[i].expect) - 1:
                        linked.CHAIN[i].output = res
            else:
                linked.CHAIN[i].output = res
            
            if stderr.getvalue():
                s_printer.return_code = 99
                thread1.join()
                node_dict = node_to_dict(linked.CHAIN[i], stdout.getvalue(), stderr.getvalue())
                print(json.dumps(node_dict, indent=4))
                print()

                return result
            else:
                s_printer.return_code = 0
                thread1.join()
                node_dict = node_to_dict(linked.CHAIN[i], stdout.getvalue(), stderr.getvalue())
                print(json.dumps(node_dict, indent=4))
                print()
            

    result = True

    return result

