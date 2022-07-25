*******
scripts
*******

.. code-block:: yaml

    scripts:
        <script_name>: <base64_encoded_script>

Scripts are distinct atomic functionalities of an ATLAS rule, like *functions* of the functional programming languages.


.. note::

    Currently Python and Powershell are supported. Javascript support is in the backlog.


Key-Value
=========

A key can be an arbitrary keyword or the function name of the entry point in the script. First, it tries to call the **key**. Then, if it fails, it calls the **run**.

.. note::

    The value must be base64 encoded. 

.. code-block:: yaml

    scripts:
        # def printer(*args) -> bool:

        #     print(" ".join(args))
        #     return True
        s1: "ZGVmIHByaW50ZXIoKmFyZ3MpIC0+IGJvb2w6CgogICAgcHJpbnQoIiAiLmpvaW4oYXJncykpCiAgICByZXR1cm4gVHJ1ZQ=="

.. code-block:: python

    import base64

    with open('script.py', 'rb') as file:
        data = file.read()

    encoded_script = base64.b64encode(data)


.. code-block:: powershell

    # It is important to give -Encoding as UTF8 instead of directly getting Byte.
    # The byte option appends byte order marker at the beginning thus ruins everthing
    $content = Get-Content .\script.ps1 -Raw -Encoding UTF8
    [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))
   
Python's execution
==================

**python_executor** function inside the core library is used. The function gets the script as base64 encoded, the script's name and arguments to pass to its entry point.

* It does in-memory import for the script.
* Calls the entry point.
* Gets the return data.


Null Bytes
==========

If the script contains null bytes, they must be encoded in the script:

.. code-block:: python
    :caption: Problematic script example

    def run(data: bytes) -> bool:
        try:
            keyIL = re.search(b'(?<=((\x72)[\x00-\xff]{4}(\x80)[\x00-\xff]{4}(\x72)))[\x00-\xff]{4}', data).group()
            su = re.search(b'[\x00-\xff]{4}(?=([\x00-\xff]{4}(\x23\x55\x53\x00)))', data).group()
        except:
            return False

        return True

When ATLAS tries to execute a rule that contains the above function as a _script_, the base64 module will raise an exception due to null bytes.

.. code-block:: python
    :caption: Null byte solution

    def run(data: bytes) -> bool:
        try:
            keyIL_encoded = b'KD88PSgocilbAC3/XXs0fSiAKVsALf9dezR9KHIpKSlbAC3/XXs0fQ=='
            su_encoded = b'WwAt/117NH0oPz0oWwAt/117NH0oI1VTACkpKQ=='
            keyIL = re.search(b64decode(keyIL_encoded), data).group()
            su = re.search(b64decode(su_encoded), data).group()
        except:
            return False

Powershell's Execution
======================

**powershell_executor** function inside the core library is used. The function gets the script as base64 encoded, the script's name and arguments to pass to its entry point.

* Creates a Powershell process. 
* Inside this process;
    * Decodes the script and creates a ScriptBlock.
    * Prepares the arguments.
    * Calls the entry point.
    * Base64 encodes the return data.
    * Creates TemporaryFile, prints the path, and writes encoded data to the file.
    * Stores the encoded data to the file.
* In Python, it reads the file and decodes it.

.. note::

    Right now **str** and **bytes** type arguments are supported for powershell execution.

