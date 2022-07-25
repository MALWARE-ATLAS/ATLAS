****
meta
****

.. code-block:: yaml

   meta:
    <key>: <value>

This section contains metadata of the rule. This is similar to YARA's meta section.

.. code-block:: yaml

   meta:
    name: "Simple"
    description: "Simple description to describe the simple rule."
    version: "1.0"

    chain:
    printer:
        input: 'Simple.'
        func: printer