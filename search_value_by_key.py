from __future__ import print_function
from typing import Dict
from pprint import pprint
import json


def replace_values(data: Dict, key: str) -> Dict:
    values = []

    def _decode_dict(a_dict):
        try:
            if a_dict.get(key):
                values.append(a_dict[key])
        except KeyError:
            pass
        return a_dict
    
    def _decode(data):
        if isinstance(data, list):
            for item in data:
                return _decode(item)
        elif isinstance(data, dict):
            return _decode_dict(data)
        return data
    
    data = json.loads(json.dumps(data), object_hook=_decode)
    return data


if __name__ == "__main__":
    with open("sample.json") as f:
        data = json.load(f)

    data = replace_values(data, "key")

    pprint(data)