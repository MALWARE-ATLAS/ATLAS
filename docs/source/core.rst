*******************
Core Library
*******************

The library that does the actual execution.

.. py:function:: reverse(...)

  Returns the reverse of the argument.

  :param any data: The data to be reversed.
  :return: Reversed data.

.. py:function:: download_from_remote_server(...)

  Downloads from the server that is passed as a argument.

  :param str addr: Address of the server.
  :return: Bytes object of the response.

.. py:function:: powershell_executor(...)

  Executes the powershell script that is passed as a argument.

  :param tuple script_name: Tuple object, script's name and base64 encoded content. It is enough to pass script key.
  :param any *args: Arguments to pass corresponding script.
  :return: Return data of the execution.

.. py:function:: file_read_bin(...)

  Performs binary file read operation.

  :param str path: File's path.
  :return: Bytes object of the file's content.

.. py:function:: file_read_utf8(...)

  Performs utf8 file read operation.

  :param str path: File's path.
  :return: The file's content.

.. py:function:: save_file_bytes(...)

  Performs binary file write operation.

  :param any data: Content to save.
  :param str prefix: File's name prefix.
  :return: Bool, condition of the operation.

.. py:function:: save_file_arr(...)

  Performs file write one by one according to the list type argument.

  :param list arr: List of contents to save.
  :param str prefix: File's name prefix. Default value is 'output'.
  :return: Bool, condition of the operation.

.. py:function:: python_executor(...)

  Executes the python script that is passed as an argument. 

  :param tuple script_name: Tuple object, script's name and base64 encoded content. It is enough to pass script key.
  :param any *args: Arguments to pass corresponding script.
  :return: Return data of the execution.

.. py:function:: printer(...)

  Prints the arguments by joining them.

  :param any *args: Strings to print.
  :return: Bool, condition of the operation.

.. py:function:: hello_world(...)

  Prints "Hello World, ATLAS." string. Can be used as a test.

  :return: None.

.. py:function:: bytes_to_str_utf8(...)

  UTF8 decodes byte object. 

  :param bytes data: Bytes data.
  :return: UTF8 string.

.. py:function:: get_sha256(...)

  Calculates sha256 checksum.

  :param bytes data: Bytes data.
  :return: sha256 checksum.