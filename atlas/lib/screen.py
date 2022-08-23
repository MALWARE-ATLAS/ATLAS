import os
import json
import time
import pprint

from typing import Dict, List

class printer:
    return_code = -1
    rows = -1
    columns = -1
    search = 0
    dTot = 0
    dCur = 0
    plat = None

    atlas_banner = \
        """             .:                                 ;.           
           ;xkl'                              .,ox;          
         .cOd,kK0k                          0xcl.cxl.        
        .lOl. .:dOko;..                 .':okd:. doko.       
        ckc.    .'cdkOxol:,,'.....',;:ldxkdc'.    dx0l.      
       ,ko.         .':loxkkkkkkkkkkxdl:,.        .k0k;      
      .lx'                x0KKKK00k:               ,xoc.     
      .dl                    l33t                  ,l.c.     
      .d:                     ''                     .;'     
      .o;                                            o,.     
      .::.                                           .0.     
      .lxl.                                          .c.     
      .lOl.                                         ,;K.     
       .okc.                                       lO,x      
        .oOxc.                .;cddl'             .oOl.      
         .l0KOo.             .d00KKKk,           .lx:.       
          .l0K0xclooc;;:cc:,;d0KKKK0x'       .'cdOd'         
           .ck0KKKKKK00KKKK00KKKKK0d,.....  ,x0KOl.          
             .:ldkO0000KKKKKKKK00K0OxxxkkkdokK0k:.           
                 ...';dxxOKKK0KK0KKKK000KKK0Oxc.             
                     .lOxdxO0KKK000Od;;:::;,..               
                      'xK0OO0KKK0kl'                         
                       c0KKKKKKKKO:                          
                       ;OKKKKKKK0o.                          
                       cOKKKKKKKOc..',,;;;,'.                
                      cO0KKKKKKK0OkO0000K000kl.              
                     .xKKKKKKKKKKKKKKKKKKKKKKx.              
                     .dKKKKKKKK0KKK00Oxk0KKKO:               
                      'x0KKKKK00kl:;,';x0KK0l.               
                       'x0KKKKKKx.   .oKKK0l.                
                        'd0KKKKK0:   .xKK0l.                 
                         'x0KKKK0l.  ,kKOc.                  
            .:c;.  ..,cldxO0KKKK0l  .d00l.                   
        .,:ok0K0OxxkO0KK0000KK00x' .o0K0o;..                 
        .,;;;;;;;;;;;;;;;;;;;;,..  .clllll:,.                """


    def __init__(self, 
                 is_banner: bool=True) -> None:
        if is_banner:
            print('\033[2J\033[1;1H')
            print(self.atlas_banner)
            print()
            print('\033[1m' + "        ATLAS - Malware Analysis Description" + '\033[0m')
            print()

    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    def status(self, 
               subchain: str,
               tab_count: int=0) -> None:

        while self.return_code == -1:
            print('\t' * tab_count + f"[|] {subchain}" + '\033[0m', end='\r')
            time.sleep(0.1)
            print('\t' * tab_count + f"[/] {subchain}" + '\033[0m', end='\r')
            time.sleep(0.1)
            print('\t' * tab_count + f"[-] {subchain}" + '\033[0m', end='\r')
            time.sleep(0.1)
            print('\t' * tab_count + f"[\\] {subchain}" + '\033[0m', end='\r')
            time.sleep(0.1)
            print('\t' * tab_count + f"[|] {subchain}" + '\033[0m', end='\r')
            time.sleep(0.1)
        if self.return_code == 0:
            print('\t' * tab_count + '\033[92m' + f"[+] " + subchain + '\033[0m')
        else:
            print('\t' * tab_count + '\033[91m' + f"[+] " + subchain + '\033[0m')
        self.return_code = -1

    
    def json_dumps(self,
                   node_dict: dict,
                   indent: int=4) -> None:
        print(json.dumps(self.excerpt(node_dict), indent=indent))
        print()


    @staticmethod
    def excerpt(node_dict: dict) -> dict:
        result = {
            'func': '',
            'input': [],
            'expect': [],
            'output': None
        }

        try:
            result['func'] = node_dict['func']
            result['expect'] = node_dict['expect']
            
            for i in node_dict['input']:
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

            if type(node_dict['output']) == str:
                result['output'] = node_dict['output'][:50]
            elif type(node_dict['output']) == int:
                result['output'] = int(str(node_dict['output'])[:50])
            elif type(node_dict['output']) == bytes:
                result['output'] = str(node_dict['output'][:50])
            elif type(node_dict['output']) == bool:
                result['output'] = node_dict['output']
            else:
                result['output'] = str(type(node_dict['output']))
            

            result['stdout'] = node_dict['stdout'][:200]
            result['stderr'] = node_dict['stderr'][:200]
        except Exception as e:
            print(e)
        
        return result