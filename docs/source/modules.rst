*******
modules
*******

.. code-block:: yaml

    modules:
        - <path_of_the_module_relative_to_process>


At its very best, ATLAS is a solution to the lack of memory. Because of that, it follows modular design paradigms.

A rule can reference other rules and re-used its components. This way, it is possible to create library-like rules for centralized analysis memory.

modules is a list, and each value references other modules by a path. After defining them, they can be used in the chain section:

.. code-block:: yaml
    :caption: decryption_lib.atl

    scripts:
    s1: "ZGVmIHJ1bihkYXRhOiBzdHIsIHhvcl9rZXk6IHN0cikgLT4gc3RyOgogICAgcmVzdWx0ID0gIiIKICAgIGtleSA9IGludCh4b3Jfa2V5LCAxNikKICAgIGZvciBpIGluIGRhdGE6CiAgICAgICAgcmVzdWx0ID0gY2hyKG9yZChpKSBeIGtleSkKCiAgICByZXR1cm4gcmVzdWx0"

    chain:
        xor_decrpytion:
            input: 
                - $scripts.s1
                - '0x30'
            func: python_executor

.. code-block:: yaml
    :caption: xor.atl
    
    meta:
        name: "Decrytion rule"
        description: "A rule to decrypt."
        version: "1.0"

    modules:
        - ATLAS/decryption_lib

    chain:
        file_read:
            input: $param.file
            func: file_read_bin

        decryption_routine: $decryption_lib.chain.xor_decryption

        printer:
            input: $decryption_routine
            func: printer

.. note::

    Right now module's path is relative to the process, but this will change in the future to be relative to the main rule's path.