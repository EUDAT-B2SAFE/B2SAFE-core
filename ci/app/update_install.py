#!/usr/bin/env python
import sys
import json
import platform
import uuid


def update_hostname(value, id):
    isstr = False
    if sys.version_info >= (3, 0):
        isstr = isinstance(value, str)
    else:
        isstr = isinstance(value, str) or isinstance(value, unicode)
    if isstr:
        return value.format(HOSTNAME=platform.node(),
                            UUID=id)
    else:
        return value


fname = sys.argv[1]
overlay_fname = sys.argv[2]
overlay_uuid = str(uuid.uuid4())

with open(overlay_fname, "r") as fp:
    overlay = json.load(fp)
overlay = {k: update_hostname(v, overlay_uuid)
           for k, v in overlay.items()}

with open(fname, "r") as fp:
    data = json.load(fp)

data.update(overlay)

with open(fname, "w") as fp:
    data = json.dump(data, fp)
