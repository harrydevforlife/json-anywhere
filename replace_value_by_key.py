from __future__ import print_function
from typing import List, Any, Dict, Union
from pathlib import Path
import json


def replace_values(
        data: Union[Dict, List],
        key: str, 
        old_value: Any, 
        new_value: Any
    ) -> Union[Dict, List]:
    """
    Replace values in a json file by searching for a key.

    :param Dict data: The data to be modified
    :param str key: The key to search for
    :param Any old_value: The value to be replaced
    :param Any new_value: The value to replace with
    :return: The modified data
    """

    def _decode_dict(a_dict):
        try:
            if a_dict.get(key) == old_value:
                a_dict[key] = new_value
        except KeyError:
            pass
        return a_dict

    def _decode_list(a_list):
        return [_decode(item) for item in a_list]
    
    def _decode(data):
        if isinstance(data, list):
            return _decode_list(data)
        elif isinstance(data, dict):
            return _decode_dict(data)
        return data
    
    data = json.loads(json.dumps(data), object_hook=_decode)
    return data


def asset_manager(
        source_file: str, 
        target_file: str,
        contexts: List[Dict]
    ) -> None:
    """
    Pass a list of contexts to replace values in a json file.

    :param str file: The path to the file to be modified
    :param Dict data: The data to be modified
        .e.g. {
            "key": "value" or ["value1", "value2"],
            "values": {
                "old": ...,
                "new": ...
            }
        }
    """
    with open(source_file) as f:
        data = json.load(f)

    for context in contexts:
        if isinstance(context["key"], str):
            context["key"] = [context["key"]]
        for key in context["key"]:
            data = replace_values(data, key, context["values"]["old"], context["values"]["new"])

    with open(target_file, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)


if __name__ == "__main__":

    contexts = [
        {
            "key": ["groupid"],
            "values": {
                "old": "f7d52023-86d9-4614-90e8-b6ea66e7aa40",
                "new": "0e44d45c-7fac-4bb2-85b4-ae4804bc224a"
            }
        },

    ]

    asset_manager(
        Path("source.json").resolve(),
        Path("target.json").resolve(),
        contexts
    )