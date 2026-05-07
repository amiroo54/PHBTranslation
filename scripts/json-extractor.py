import json
import sys

j = json.loads(open(sys.argv[1]).read())

"""
for obj in j["variantrule"]:
    try:
        if obj["source"] != "XPHB":
            continue
    except:
        continue
    print(obj["name"])
"""

for obj in j["data"]:
    if obj["type"] == "section":
        print(obj["name"])
        for chi in obj["entries"]:
            try:
                if chi["type"] == "section":
                    print(chi["name"])
            except:
                continue
