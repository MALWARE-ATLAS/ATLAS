*******************
Rule
*******************

ATLAS rules or atl files follow YAML syntax. It has at most 4 keys: **meta**, **modules**, **scripts** and **chain**.

.. code-block:: yaml

    meta:
        name: "Hello World"
        description: "Traditional way to start."
        version: "1.0"

    chain:
        printer_subchain:
            input: 'Hello World, P.S. ATLAS.'
            func: printer

.. note::

    **chain** is the only section that a valid rule must contain.
