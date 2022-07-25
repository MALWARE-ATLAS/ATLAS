*****
chain
*****

.. code-block:: yaml

    chain:
        <sub-chain_name>:
            input: <input>
            func: <function_name_from_core>

This section is a description of the rule's execution. **chain** consists of one or more sub-chains. It is like a linked list.

.. code-block:: yaml

    chain:
        file_read:
            input: <path>
            func: file_read_bin
        save_file:
            input: $file_read
            func: save_file_bytes

.. note::

    For the above example, **file_read** and **save_file** are sub-chains.


Sub-chain
=========

A sub-chain can be thought like a function. It takes inputs, processes them, and gives output.

The keyword that defines a sub-chain is just arbitrary, like variable names.

.. note::

    Sub-chain key mustn't be one of the special keys like **chain**, **scripts**, etc.

Sub-chains are executed one by one unless it catches an exception or fails to expect satisfaction if there is any. So it is safe to assume that there is AND relation between same-level sub-chains.

When a step isn't singular, and there are a bunch of variations, OR block might be a solution. It is a sub-chain that has inner sub-chains instead of func details. In this way, the execution continues one by one until the expectation is satisfied. If there is none, then the execution is stopped immediately.

.. note::

    It is a must to define expect key for OR blocks.

To create OR relation, it should be defined inner-subchains:

.. code-block:: yaml
    :caption: remcos.atl

    meta:
        name: "Remcos"
        description: "A rule to process Remcos png files"
        reference: "https://r00tten.com/in-depth-analysis-attack-vector-triggered-by-risk/"
        version: "1.0"

    scripts:
        png_extract: "ZnJvbSB0eXBpbmcgaW1wb3J0IERpY3QsIExpc3QKCmRlZiBydW4oZGF0YTogYnl0ZXMpIC0+IExpc3RbYW55XToKICAgIGFyck0gPSBbMHg4OSwgMHg1MCwgMHg0RSwgMHg0NywgMHgwRCwgMHgwQSwgMHgxQSwgMHgwQSwgMHgwMCwgMHgwMCwgMHgwMF0KICAgIGFyclQgPSBbMHg0OSwgMHg0NSwgMHg0RSwgMHg0NCwgMHhBRSwgMHg0MiwgMHg2MCwgMHg4Ml0KCiAgICBzdGF0dXMgPSBGYWxzZQogICAgc3RhcnQgPSAtMQogICAgYXJyUCA9IFtdCiAgICBmb3IgaSBpbiByYW5nZShsZW4oZGF0YSkpOgogICAgICAgIGlmIHN0YXR1cyA9PSBGYWxzZToKICAgICAgICAgICAgZm9yIGogaW4gcmFuZ2UobGVuKGFyck0pKToKICAgICAgICAgICAgICAgIGlmIGxlbihkYXRhKSA8IGkgKyBsZW4oYXJyTSk6CiAgICAgICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICAgICAgICAgIGVsaWYgaiA9PSBsZW4oYXJyTSkgLSAxOgogICAgICAgICAgICAgICAgICAgIGlmIGFyck1bal0gPT0gZGF0YVtqICsgaV06CiAgICAgICAgICAgICAgICAgICAgICAgIHN0YXJ0ID0gaQogICAgICAgICAgICAgICAgICAgICAgICBzdGF0dXMgPSBUcnVlCiAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAgIGlmIGFyck1bal0gIT0gZGF0YVtqICsgaV06CiAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgZWxzZToKICAgICAgICAgICAgZm9yIGsgaW4gcmFuZ2UobGVuKGFyclQpKToKICAgICAgICAgICAgICAgIGlmIGxlbihkYXRhKSA8IGkgKyBsZW4oYXJyTSk6CiAgICAgICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICAgICAgICAgIGVsaWYgayA9PSBsZW4oYXJyVCkgLSAxOgogICAgICAgICAgICAgICAgICAgIGlmIGFyclRba10gPT0gZGF0YVtrICsgaV06CiAgICAgICAgICAgICAgICAgICAgICAgIGFyclAuYXBwZW5kKGRhdGFbc3RhcnQ6ayArIGkgKyAxXSkKICAgICAgICAgICAgICAgICAgICAgICAgc3RhcnQgPSAtMQogICAgICAgICAgICAgICAgICAgICAgICBzdGF0dXMgPSBGYWxzZQogICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgICAgICBpZiBhcnJUW2tdICE9IGRhdGFbayArIGldOgogICAgICAgICAgICAgICAgICAgICAgICBicmVhawogICAgCiAgICByZXR1cm4gYXJyUA=="
        find_signature: "aW1wb3J0IHJlCmRlZiBkb3RuZXRfbm9uZV9zdHJ1Y3RfZmluZFNpZ25hdHVyZUFkZHJfMShkYXRhOiBieXRlcykgLT4gYnl0ZXM6CiAgICBhZGRyID0gYicnCgogICAgdHJ5OgogICAgICAgIGFkZHIgPSByZS5zZWFyY2goYidCU0pCJywgZGF0YSkuc3BhbigpWzBdCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgbG9nZ2luZy5lcnJvcihlKQogICAgCiAgICByZXR1cm4gYWRkcg=="
        get_key: "aW1wb3J0IHJlCgpmcm9tIFBJTCBpbXBvcnQgSW1hZ2UKZnJvbSBiYXNlNjQgaW1wb3J0IGI2NGRlY29kZQoKCmRlZiBydW4oZGF0YSk6CiAgICBpZiBkYXRhID09IE5vbmU6CiAgICAgICAgcmV0dXJuIEZhbHNlCiAgICAKICAgIHRyeToKICAgICAgICBrZXlJTF9lbmNvZGVkID0gYidLRDg4UFNnb2NpbGJBQzMvWFhzMGZTaUFLVnNBTGY5ZGV6UjlLSElwS1NsYkFDMy9YWHMwZlE9PScKICAgICAgICBzdV9lbmNvZGVkID0gYidXd0F0LzExN05IMG9QejBvV3dBdC8xMTdOSDBvSTFWVEFDa3BLUT09JwogICAgICAgIGJhc2VfZW5jb2RlZCA9IGInUWxOS1FnPT0nCiAgICAgICAga2V5SUwgPSByZS5zZWFyY2goYjY0ZGVjb2RlKGtleUlMX2VuY29kZWQpLCBkYXRhKS5ncm91cCgpCiAgICAgICAgc3UgPSByZS5zZWFyY2goYjY0ZGVjb2RlKHN1X2VuY29kZWQpLCBkYXRhKS5ncm91cCgpCiAgICAgICAgYmFzZSA9IHJlLnNlYXJjaChiNjRkZWNvZGUoYmFzZV9lbmNvZGVkKSwgZGF0YSkuc3BhbigpWzBdCiAgICBleGNlcHQ6CiAgICAgICAgcmV0dXJuIEZhbHNlCgogICAgYWRkciA9IGludC5mcm9tX2J5dGVzKHN1LCAnbGl0dGxlJykgKyBiYXNlICsgKGludC5mcm9tX2J5dGVzKGtleUlMLCAnbGl0dGxlJykgJiAweDAwZmZmZmZmKQogICAgbGVuZ3RoID0gZGF0YVthZGRyXQogICAgCiAgICBudWxsX2J5dGVfZW5jb2RlZCA9IGInQUE9PScKICAgIGtleSA9IFtdCiAgICBrZXkuYXBwZW5kKGRhdGFbYWRkciArIDE6YWRkciArIDEgKyBsZW5ndGhdKQogICAga2V5LmFwcGVuZChrZXlbMF0uZGVjb2RlKCdhc2NpaScsIGVycm9ycz0naWdub3JlJykucmVwbGFjZShiNjRkZWNvZGUobnVsbF9ieXRlX2VuY29kZWQpLmRlY29kZSgndXRmLTgnKSwgJycpLmVuY29kZSgndXRmOCcsIGVycm9ycz0naWdub3JlJykpCiAgICBrZXkuYXBwZW5kKGtleVswXS5kZWNvZGUoJ2FzY2lpJywgZXJyb3JzPSdpZ25vcmUnKS5yZXBsYWNlKGI2NGRlY29kZShudWxsX2J5dGVfZW5jb2RlZCkuZGVjb2RlKCd1dGYtOCcpLCAnJykuZW5jb2RlKCd1dGYtMTYtYmUnKSkKCiAgICByZXR1cm4ga2V5"
        1pxHeightImageProcess: "aW1wb3J0IGlvCmltcG9ydCBoYXNobGliCmZyb20gUElMIGltcG9ydCBJbWFnZQoKCmRlZiBydW4oYXJyKToKICAgIGRhdGEgPSBbXQoKICAgIGZvciBpIGluIGFycjoKICAgICAgICBpbSA9IEltYWdlLm9wZW4oaW8uQnl0ZXNJTyhpKSkgCiAgICAgICAgd2lkdGgsIGhlaWdodCA9IGltLnNpemUKICAgICAgICBwaXggPSBpbS5sb2FkKCkKICAgICAgICBkYXRhID0gaW0uZ2V0ZGF0YSgpCiAgICAgICAgCiAgICAgICAgYXJyID0gW10KICAgICAgICBmb3IgaSBpbiByYW5nZShoZWlnaHQpOgogICAgICAgICAgICBmb3IgaiBpbiByYW5nZSh3aWR0aCk6CiAgICAgICAgICAgICAgICByZWQgPSBwaXhbaiwgaV1bMF0KICAgICAgICAgICAgICAgIGdyZWVuID0gcGl4W2osIGldWzFdCiAgICAgICAgICAgICAgICBibHVlID0gcGl4W2osIGldWzJdCiAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgIGFyci5hcHBlbmQoKHJlZCArIChncmVlbiAqIDI1NikgKyAoYmx1ZSAqIDI1NiAqIDI1NikpKQogICAgICAgIAogICAgICAgIGlmIGFycls6Ml0gPT0gWzc3LCA5MF06CiAgICAgICAgICAgIGRhdGEgPSBieXRlYXJyYXkoYXJyKQogICAgICAgICAgICBicmVhawoKICAgIHJldHVybiBkYXRh"
        1000pxImageProcess: "aW1wb3J0IGlvCmltcG9ydCBoYXNobGliCmZyb20gUElMIGltcG9ydCBJbWFnZQoKCmRlZiBydW4oYXJyKToKICAgIGRhdGEgPSBbXQoKICAgIGZvciBpbWFnZSBpbiBhcnI6CiAgICAgICAgaW0gPSBJbWFnZS5vcGVuKGlvLkJ5dGVzSU8oaW1hZ2UpKQogICAgICAgIHdpZHRoLCBoZWlnaHQgPSBpbS5zaXplCiAgICAgICAgdHJ5OgogICAgICAgICAgICBwaXggPSBpbS5sb2FkKCkKICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgIHJldHVybiBkYXRhCiAgICAgICAgCiAgICAgICAgYXJyID0gW10KICAgICAgICBmb3IgaSBpbiByYW5nZShoZWlnaHQpOgogICAgICAgICAgICBmb3IgaiBpbiByYW5nZSh3aWR0aCk6CiAgICAgICAgICAgICAgICBpZiBwaXhbaiwgaV0gIT0gKDAsIDAsIDAsIDApOgogICAgICAgICAgICAgICAgICAgIGFyci5hcHBlbmQocGl4W2osIGldWzBdKQogICAgICAgICAgICAgICAgICAgIGFyci5hcHBlbmQocGl4W2osIGldWzFdKQogICAgICAgICAgICAgICAgICAgIGFyci5hcHBlbmQocGl4W2osIGldWzJdKQogICAgICAgIAogICAgICAgIGFyckIgPSBbXQogICAgICAgIGZvciBqIGluIHJhbmdlKDMyKToKICAgICAgICAgICAgYXJyQi5hcHBlbmQoaW50KGFycltqXSAlIDIgPT0gMSkpCiAgICAgICAgCiAgICAgICAgYXJyQl9yZXZlcnNlZCA9IGFyckJbOjotMV0KICAgICAgICBzaXplID0gaW50KCIiLmpvaW4oc3RyKGkpIGZvciBpIGluIGFyckJfcmV2ZXJzZWQpLCAyKQogICAgICAgIAogICAgICAgIGFyckIyID0gW10KICAgICAgICBmb3IgayBpbiByYW5nZSgzMiwgbGVuKGFycikpOgogICAgICAgICAgICBhcnJCMi5hcHBlbmQoaW50KGFycltrXSAlIDIgPT0gMSkpCgogICAgICAgIGFyckIyX3JldmVyc2VkID0gYXJyQjJbOjotMV0KICAgICAgICBhcnJJTSA9IFtdCiAgICAgICAgZm9yIHogaW4gcmFuZ2UoaW50KGxlbihhcnJCMl9yZXZlcnNlZCkgLyA4KSAtIDEsIDAsIC0xKToKICAgICAgICAgICAgYXJySU0uYXBwZW5kKGludCgiIi5qb2luKHN0cihpKSBmb3IgaSBpbiBhcnJCMl9yZXZlcnNlZFt6ICogODp6ICogOCArIDhdKSwgMikpCiAgICAgICAgCiAgICAgICAgdHJ5OgogICAgICAgICAgICBpbTIgPSBJbWFnZS5vcGVuKGlvLkJ5dGVzSU8oYnl0ZWFycmF5KGFycklNKSkpCiAgICAgICAgICAgIHdpZHRoMiwgaGVpZ2h0MiA9IGltMi5zaXplCiAgICAgICAgICAgIHBpeDIgPSBpbTIubG9hZCgpCiAgICAgICAgZXhjZXB0OgogICAgICAgICAgICByZXR1cm4gZGF0YQoKICAgICAgICBhcnIyID0gW10KICAgICAgICBmb3IgaSBpbiByYW5nZSh3aWR0aDIpOgogICAgICAgICAgICBmb3IgaiBpbiByYW5nZShoZWlnaHQyKToKICAgICAgICAgICAgICAgIGlmIHBpeFtpLCBqXSAhPSAoMCwgMCwgMCwgMCk6CiAgICAgICAgICAgICAgICAgICAgYXJyMi5hcHBlbmQocGl4MltpLCBqXVsyXSkKICAgICAgICAgICAgICAgICAgICBhcnIyLmFwcGVuZChwaXgyW2ksIGpdWzFdKQogICAgICAgICAgICAgICAgICAgIGFycjIuYXBwZW5kKHBpeDJbaSwgal1bMF0pCiAgICAgICAgICAgICAgICAgICAgYXJyMi5hcHBlbmQocGl4MltpLCBqXVszXSkKCiAgICAgICAgaWYgYXJyMls0OjZdID09IFs3NywgOTBdOgogICAgICAgICAgICBkYXRhID0gYnl0ZWFycmF5KGFycjJbNDpdKQogICAgICAgICAgICBicmVhawoKICAgIHJldHVybiBkYXRh"
        gzipImageProcess: "aW1wb3J0IGlvCmltcG9ydCBnemlwCmltcG9ydCBoYXNobGliCmZyb20gUElMIGltcG9ydCBJbWFnZQoKCmRlZiBydW4oYXJyLCBrZXkpOgogICAgZGF0YSA9IHt9CiAgICBwcmludChsZW4oYXJyKSkKICAgIHByaW50KGtleSkKICAgIGZvciBpbWFnZSBpbiBhcnI6CiAgICAgICAgaW0gPSBJbWFnZS5vcGVuKGlvLkJ5dGVzSU8oaW1hZ2UpKQogICAgICAgIHdpZHRoLCBoZWlnaHQgPSBpbS5zaXplCiAgICAgICAgdHJ5OgogICAgICAgICAgICBwaXggPSBpbS5sb2FkKCkKICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgIHJldHVybiBkYXRhCgogICAgICAgIGFyciA9IFtdCiAgICAgICAgZm9yIGkgaW4gcmFuZ2Uod2lkdGgpOgogICAgICAgICAgICBmb3IgaiBpbiByYW5nZShoZWlnaHQpOgogICAgICAgICAgICAgICAgaWYgcGl4W2ksIGpdICE9ICgwLCAwLCAwLCAwKToKICAgICAgICAgICAgICAgICAgICBhcnIuYXBwZW5kKHBpeFtpLCBqXVswXSkKICAgICAgICAgICAgICAgICAgICBhcnIuYXBwZW5kKHBpeFtpLCBqXVsxXSkKICAgICAgICAgICAgICAgICAgICBhcnIuYXBwZW5kKHBpeFtpLCBqXVsyXSkKICAgICAgICAKICAgICAgICBhcnJFID0gYXJyCgogICAgICAgIG51bTQgPSBhcnJFW2xlbihhcnJFKSAtIDFdIF4gMTEyCgogICAgICAgIGZvciBpIGluIGtleToKICAgICAgICAgICAgeEtleSA9IGkKICAgICAgICAgICAgYXJyRCA9IFtdCgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBmb3IgayBpbiByYW5nZShsZW4oYXJyRSkpOgogICAgICAgICAgICAgICAgICAgIGFyckQuYXBwZW5kKGFyckVba10gXiBudW00IF4geEtleVtrICUgbGVuKHhLZXkpXSkKICAgICAgICAgICAgZXhjZXB0IFplcm9EaXZpc2lvbkVycm9yOgogICAgICAgICAgICAgICAgcmV0dXJuIGRhdGEKICAgICAgICAgICAgCiAgICAgICAgICAgIGZvciBpIGluIHJhbmdlKGxlbihhcnJEKSwgMCwgLTEpOgogICAgICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgICAgIGlmIGFyckRbaV0gPT0gYXJyRFswXSBhbmQgYXJyRFtpICsgMV0gPT0gYXJyRFsxXToKICAgICAgICAgICAgICAgICAgICAgICAgYXJyRFtpOl0gPSBhcnJEWzo0XQogICAgICAgICAgICAgICAgICAgICAgICBicmVhawogICAgICAgICAgICAgICAgZXhjZXB0OgogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGRlY29tcHJlc3MgPSBnemlwLmRlY29tcHJlc3MoYnl0ZWFycmF5KGFyckRbNDpdKSkKCiAgICAgICAgICAgICAgICBpZiBkZWNvbXByZXNzWzoyXSA9PSBiJ01aJzoKICAgICAgICAgICAgICAgICAgICBkYXRhID0gZGVjb21wcmVzcwogICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgICAgIGNvbnRpbnVlCgogICAgcmV0dXJuIGRhdGE="
        run: "ZnVuY3Rpb24gcnVuKCRpbWFnZV9kYXRhLCAka2V5KSB7DQogICAgQWRkLUNvbnRlbnQgYzpcXFVzZXJzXFxKb2huXFxEZXNrdG9wXFx0ZXN0LnR4dCAtVmFsdWUgIlRoZSBydW4gZnVuY3Rpb24gaXMgc3RhcnRpbmciDQogICAgI1NldC1Db250ZW50IC1FbmNvZGluZyBCeXRlIC1WYWx1ZSAkaW1hZ2VfZGF0YSBjOlxcVXNlcnNcXEpvaG5cXERlc2t0b3BcXHRlc3QucG5nDQogICAgI1NldC1Db250ZW50IC1WYWx1ZSAka2V5IGM6XFxVc2Vyc1xcSm9oblxcRGVza3RvcFxcdGVzdC50eHQNCiAgICB0cnkNCiAgICB7DQogICAgICAgICRtZW1vcnlfc3RyZWFtID0gbmV3LW9iamVjdCBTeXN0ZW0uSU8uTWVtb3J5U3RyZWFtKCwkaW1hZ2VfZGF0YSkNCiAgICAgICAgQWRkLUNvbnRlbnQgYzpcXFVzZXJzXFxKb2huXFxEZXNrdG9wXFx0ZXN0LnR4dCAtVmFsdWUgIm1lbW9yeV9zdHJlYW0iDQogICAgICAgICRCaXRtYXAgPSBbU3lzdGVtLkRyYXdpbmcuSW1hZ2VdOjpGcm9tU3RyZWFtKCRtZW1vcnlfc3RyZWFtKTsNCiAgICAgICAgQWRkLUNvbnRlbnQgYzpcXFVzZXJzXFxKb2huXFxEZXNrdG9wXFx0ZXN0LnR4dCAtVmFsdWUgIkJpdG1hcCINCiAgICAgICAgJGJ5dGVfYXJyYXkgPSBbQmFzaWNUZXN0XTo6Y2JhKCRCaXRtYXApDQogICAgICAgIEFkZC1Db250ZW50IGM6XFxVc2Vyc1xcSm9oblxcRGVza3RvcFxcdGVzdC50eHQgLVZhbHVlICJieXRlX2FycmF5Ig0KICAgICAgICAkc291cmNlX2ZpbGUgPSBbQmFzaWNUZXN0XTo6ZmdoKCRieXRlX2FycmF5LCAka2V5KQ0KICAgICAgICBBZGQtQ29udGVudCBjOlxcVXNlcnNcXEpvaG5cXERlc2t0b3BcXHRlc3QudHh0IC1WYWx1ZSAic291cmNlX2ZpbGUiDQogICAgICAgICNTZXQtQ29udGVudCAiQzpcVXNlcnNcSm9oblxEZXNrdG9wXFJlc291cmNlRmFsbGJhY2tNYW5hMy5iaW4iICRzb3VyY2VfZmlsZSAtRW5jb2RpbmcgQnl0ZQ0KICAgICAgICByZXR1cm4gW1N5c3RlbS5Db252ZXJ0XTo6VG9CYXNlNjRTdHJpbmcoJHNvdXJjZV9maWxlKQ0KICAgIH0NCiAgICBjYXRjaA0KICAgIHsNCiAgICAgICAgQWRkLUNvbnRlbnQgLVZhbHVlICRfIGM6XFxVc2Vyc1xcSm9oblxcRGVza3RvcFxcdGVzdC50eHQNCiAgICB9DQogICAgQWRkLUNvbnRlbnQgYzpcXFVzZXJzXFxKb2huXFxEZXNrdG9wXFx0ZXN0LnR4dCAtVmFsdWUgIlRoZSBydW4gZnVuY3Rpb24gaXMgZmluaXNoZWQiDQoNCg0KfQ0KDQokcmVmcyA9IEAoDQogICAgImM6XFByb2dyYW0gRmlsZXMgKHg4NilcUmVmZXJlbmNlIEFzc2VtYmxpZXNcTWljcm9zb2Z0XEZyYW1ld29ya1wuTkVURnJhbWV3b3JrXHY0LjBcU3lzdGVtLkRyYXdpbmcuZGxsIiwNCiAgICAiYzpcUHJvZ3JhbSBGaWxlcyAoeDg2KVxSZWZlcmVuY2UgQXNzZW1ibGllc1xNaWNyb3NvZnRcRnJhbWV3b3JrXC5ORVRGcmFtZXdvcmtcdjQuMFxNaWNyb3NvZnQuVmlzdWFsQmFzaWMuZGxsIg0KKQ0KDQokdHlwZV9kZWZpbml0aW9uID0gQCINCnVzaW5nIFN5c3RlbTsNCnVzaW5nIFN5c3RlbS5EcmF3aW5nOw0KdXNpbmcgU3lzdGVtLlRleHQ7DQp1c2luZyBTeXN0ZW0uSU87DQp1c2luZyBNaWNyb3NvZnQuVmlzdWFsQmFzaWM7DQp1c2luZyBNaWNyb3NvZnQuVmlzdWFsQmFzaWMuQ29tcGlsZXJTZXJ2aWNlczsNCg0KDQpwdWJsaWMgY2xhc3MgQmFzaWNUZXN0DQp7DQogICAgcHVibGljIHN0YXRpYyBieXRlW10gZmdoKGJ5dGVbXSBQMSwgc3RyaW5nIEsxKQ0KCQl7DQoJCQlieXRlW10gYnl0ZXMgPSBFbmNvZGluZy5CaWdFbmRpYW5Vbmljb2RlLkdldEJ5dGVzKEsxKTsNCgkJCWNoZWNrZWQNCgkJCXsNCgkJCQlpbnQgbnVtID0gKGludCkoUDFbUDEuTGVuZ3RoIC0gMV0gXiAxMTIpOw0KCQkJCWJ5dGVbXSBhcnJheSA9IG5ldyBieXRlW1AxLkxlbmd0aCArIDFdOw0KCQkJCWludCBudW0yID0gUDEuTGVuZ3RoIC0gMSArIDYgLSA2Ow0KCQkJCWludCBudW0zID0gbnVtMjsNCgkJCQlpbnQgbnVtNCA9IDA7DQoJCQkJZm9yIChpbnQgaSA9IDA7IGkgPD0gbnVtMzsgaSsrKQ0KCQkJCXsNCgkJCQkJYXJyYXlbaSArIDIyIC0gMTEgLSAxMV0gPSAoYnl0ZSkoKGludClQMVtpICsgMjIgLSAxMSAtIDExXSBeIG51bSBeIChpbnQpYnl0ZXNbbnVtNF0pOw0KCQkJCQlpZiAobnVtNCA9PSBLMS5MZW5ndGggLSAxICsgNiAtIDYpDQoJCQkJCXsNCgkJCQkJCW51bTQgPSAwOw0KCQkJCQl9DQoJCQkJCWVsc2UNCgkJCQkJew0KCQkJCQkJbnVtNCsrOw0KCQkJCQl9DQoJCQkJfQ0KCQkJCXJldHVybiAoYnl0ZVtdKVV0aWxzLkNvcHlBcnJheShhcnJheSwgbmV3IGJ5dGVbUDEuTGVuZ3RoIC0gMiArIDEgLSAxICsgMV0pOw0KCQkJfQ0KCQl9DQoNCiAgICBwdWJsaWMgc3RhdGljIGJ5dGVbXSBjYmEoQml0bWFwIFVHaEhibkJuYVd0bFlreDEpDQoJCXsNCgkJCWludCBudW0gPSAwOw0KCQkJaW50IHdpZHRoID0gVUdoSGJuQm5hV3RsWWt4MS5TaXplLldpZHRoOw0KCQkJY2hlY2tlZA0KCQkJew0KCQkJCWludCBudW0yID0gd2lkdGggKiB3aWR0aCAqIDQ7DQoJCQkJYnl0ZVtdIGFycmF5ID0gbmV3IGJ5dGVbbnVtMiAtIDEgKyAxXTsNCgkJCQlpbnQgbnVtMyA9IHdpZHRoIC0gMiArIDE7DQoJCQkJZm9yIChpbnQgaSA9IDA7IGkgPD0gbnVtMzsgaSsrKQ0KCQkJCXsNCgkJCQkJaW50IG51bTQgPSB3aWR0aCAtIDIgKyAxOw0KCQkJCQlmb3IgKGludCBqID0gMDsgaiA8PSBudW00OyBqKyspDQoJCQkJCXsNCgkJCQkJCUJ1ZmZlci5CbG9ja0NvcHkoQml0Q29udmVydGVyLkdldEJ5dGVzKFVHaEhibkJuYVd0bFlreDEuR2V0UGl4ZWwoaSwgaikuVG9BcmdiKCkpLCAwLCBhcnJheSwgbnVtLCA0KTsNCgkJCQkJCW51bSArPSA0Ow0KCQkJCQl9DQoJCQkJfQ0KCQkJCWludCBudW01ID0gQml0Q29udmVydGVyLlRvSW50MzIoYXJyYXksIDApOw0KCQkJCWJ5dGVbXSBhcnJheTIgPSBuZXcgYnl0ZVtudW01IC0gMyArIDIgKyAxXTsNCgkJCQlCdWZmZXIuQmxvY2tDb3B5KGFycmF5LCA0LCBhcnJheTIsIDAsIGFycmF5Mi5MZW5ndGgpOw0KCQkJCXJldHVybiBhcnJheTI7DQoJCQl9DQoJCX0NCg0KfQ0KDQoiQA0KDQp0cnkNCnsNCiAgICBBZGQtVHlwZSAtUGF0aCAkcmVmcw0KICAgIEFkZC1UeXBlIC1SZWZlcmVuY2VkQXNzZW1ibGllcyAkcmVmcyAtVHlwZURlZmluaXRpb24gJHR5cGVfZGVmaW5pdGlvbiAtTGFuZ3VhZ2UgQ1NoYXJwDQogICAgQWRkLVR5cGUgLUFzc2VtYmx5TmFtZSBTeXN0ZW0uRHJhd2luZw0KfQ0KY2F0Y2gNCnsNCiAgICBBZGQtQ29udGVudCAtVmFsdWUgJF8gYzpcXFVzZXJzXFxKb2huXFxEZXNrdG9wXFx0ZXN0LnR4dA0KfQ0KDQo="


    chain:
        file_read:
            input: <path>
            func: file_read_bin

        pngExtract:
            input: 
                - $scripts.png_extract
                - $file_read
            func: python_executor

        key:
            input:
                - $scripts.get_key
                - $file_read
            func: python_executor

        pngProcess:
            expect: is_pe

            1pxHeight:
                input:
                    - $scripts.1pxHeightImageProcess
                    - $pngExtract
                func: python_executor

            1000px:
                input:
                    - $scripts.1000pxImageProcess
                    - $pngExtract
                func: python_executor

            gzip:
                input:
                    - $scripts.gzipImageProcess
                    - $pngExtract
                    - $key
                func: python_executor
            
            powershell_executor:
                input: 
                    - $scripts.run
                    - $file_read
                    - <key>
                func: powershell_executor

        save_file2:
            input: $pngProcess
            func: save_file_bytes


For the example above, the **pngProcess** sub-chain is OR block. **expect: is_pe** is the top-level key for the sub-chain. It applies to all inner sub-chains. So repeated keys can be combined in this way.

During the execution of the **pngProcess** it starts from the first inner sub-chain, which is **1pxHeight**, and continues until the expectation is satisfied.

In the OR block, the satisfying output assigns to the top-level sub-chain key rather than the inner sub-chain to solve the ambiguity. **save_file2** sub_chain references OR block's output through **$pngProcess**.
   
input
=====

A sub-chain could have zero or more inputs. An input's value might be static like a string. But it is possible to reference dynamic content through the $ prefix:

* Previous sub-chains outputs. Like the above example, **file_read**'s output is **pngExtract**'s input.
* A script,

.. code-block:: yaml

    meta:
        name: "rtf_template_injection"
        description: "A rule to extracts rtf template injection"
        version: "1.0"

    scripts:
        # import re
        # import base64
        
        # def run(data: bytes) -> str:
        #     result = ''

        #     encoded_template_pattr = "XHtcXFwqXFx0ZW1wbGF0ZVxzKyguKylccypcfQ=="
        #     try:
        #         result = re.search(base64.b64decode(encoded_template_pattr), data).group(1).decode()
        #     except Exception as e:
        #         print(e)
        #         return result

        #     return result
        s1: "aW1wb3J0IHJlCmltcG9ydCBiYXNlNjQKIApkZWYgcnVuKGRhdGE6IGJ5dGVzKSAtPiBzdHI6CiAgICByZXN1bHQgPSAnJwoKICAgIGVuY29kZWRfdGVtcGxhdGVfcGF0dHIgPSAiWEh0Y1hGd3FYRngwWlcxd2JHRjBaVnh6S3lndUt5bGNjeXBjZlE9PSIKICAgIHRyeToKICAgICAgICByZXN1bHQgPSByZS5zZWFyY2goYmFzZTY0LmI2NGRlY29kZShlbmNvZGVkX3RlbXBsYXRlX3BhdHRyKSwgZGF0YSkuZ3JvdXAoMSkuZGVjb2RlKCkKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICBwcmludChlKQogICAgICAgIHJldHVybiByZXN1bHQKCiAgICByZXR1cm4gcmVzdWx0"

    chain:
        file_read:
            input: <path>
            func: file_read_bin

        template_extract:
            input: 
                - $scripts.s1
                - $file_read
            func: python_executor

        print_template:
            input: $template_extract
            func: printer

* Key-value from command-line arguments.

.. code-block:: yaml

    meta:
        name: "Param"
        description: "Test ATLAS rule for param"

    chain:
        printer:
            input: $param.printer
            func: printer


func
====

This key holds the function name to call from the core library for the execution.

.. note::

    **func** is the only key that a valid sub-chain must contain.

expect
======

This key hold the function name to call from the expect library after the execution for validation. The corresponding sub-chain output is passed to the function. The execution is stopped if the output doesn't satisfy the expected value.

.. code-block:: yaml

    meta:
        name: "is_pe"
        description: "A rule to validate whether the input file's reverse is peexe or not."
        version: "1.0"

    chain:
        file_read:
            input: <path>
            func: file_read_bin

        pe_validation:
            input: $file_read
            func: reverse
            expect: is_pe

        save_file:
            input: $pe_validation
            func: save_file_bytes
