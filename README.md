# ATLAS

According to [Merriam-Webster](https://www.merriam-webster.com/dictionary/atlas):
>**atlas** noun </br>_at·​las_ | _at-ləs_</br></br>**1. capitalized :** a Titan who for his part in the Titans' revolt against the gods is forced by Zeus to support the heavens on his shoulders</br>**3. a :** a bound collection of maps often including illustrations, informative tables, or textual matter

---

</br>

**ATLAS** is an analysis description of malware or kill-chain. Malware is a combination of techniques crafted for a purpose. With an ATLAS rule, these techniques and capabilities are like LEGO pieces. In this way, it tries to help malware researchers to focus single piece at a time and nothing more. ATLAS interpretation of the rule does the rest. It also removes the language boundaries. Different pieces can be written in other script languages.

If these techniques are transformed into LEGO pieces properly, it eventually creates a memory. Then, the total time to write an ATLAS rule will decrease.

``` yaml
meta:
  name: "rtf_template_injection"
  description: "A rule to extracts rtf template injection"
  reference: "https://www.proofpoint.com/us/blog/threat-insight/injection-new-black-novel-rtf-template-inject-technique-poised-widespread"
  version: "1.0"

scripts:
  # import re
  # import base64
  
  # def run(data: bytes) -> str:
  #     result = ''

  #     encoded_template_pattr = "XHtcXFwqXFx0ZW1wbGF0ZVxzKyguKylccypcfQ=="
  #     result = re.search(base64.b64decode(encoded_template_pattr), data).group(1).decode()

  #     return result
  s1: "aW1wb3J0IHJlCmltcG9ydCBiYXNlNjQKIApkZWYgcnVuKGRhdGE6IGJ5dGVzKSAtPiBzdHI6CiAgICByZXN1bHQgPSAnJwoKICAgIGVuY29kZWRfdGVtcGxhdGVfcGF0dHIgPSAiWEh0Y1hGd3FYRngwWlcxd2JHRjBaVnh6S3lndUt5bGNjeXBjZlE9PSIKICAgIHJlc3VsdCA9IHJlLnNlYXJjaChiYXNlNjQuYjY0ZGVjb2RlKGVuY29kZWRfdGVtcGxhdGVfcGF0dHIpLCBkYXRhKS5ncm91cCgxKS5kZWNvZGUoKQoKICAgIHJldHVybiByZXN1bHQ="

chain:
  file_read:
    input: $param.file
    func: file_read_bin

  template_extract:
    input: 
        - $scripts.s1
        - $file_read
    func: python_executor

  download:
    input: $template_extract
    func: download_from_remote_server

  save_template:
    input: 
      - $download
      - "template_"
    func: save_file_bytes
```

When the above rule is processed by ATLAS:
* It reads the file according to command-line argument,
* Then runs the python script that is defined in **scripts** section,
* Tries to downloads the template from the matched pattern,
* And saves the downloaded data to the disk.


## Installation

Install using Python's PIP:

``` bash
pip install malware-atlas
```

Clone directly from Github:

``` bash
git clone https://github.com/malware-atlas/atlas
```


## Test Run

The [HelloWorld](https://github.com/MALWARE-ATLAS/ATLAS/blob/master/HelloWorld.atl) rule can be used to test the installation.

To test it:

``` bash
atlas -a HelloWorld.atl
```


---

To discover the full potential of the ATLAS, you could check the documentation: https://malware-atlas.readthedocs.io/en/latest/
