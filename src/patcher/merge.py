import fnmatch
import os
import typing

import json5 as json
import toml
import yaml
from src import options


class MergeError(Exception):
    ...


def merge(from_path: str, to_path: str):
    _, ext_from = os.path.splitext(from_path)
    _, ext_to = os.path.splitext(to_path)
    if ext_from != ext_to:
        raise MergeError(f'Cannot merge files with different extensions: "{from_path}" and "{to_path}"')

    for pattern, merge_func in MERGE_MAP.items():
        if fnmatch.fnmatch(to_path, pattern):
            merge_func(from_path, to_path)
            return
    raise MergeError(f'Unknown file type: "{to_path}"')


def _merge_file(
    from_path: str, to_path: str,
    loader: typing.Callable[[typing.IO], dict], dumper: typing.Callable[[dict, typing.IO], None],
    from_args: dict = None, to_args: dict = None, dump_args: dict = None
):
    '''Merge two files using the given loader and dumper functions.'''
    with open(from_path, 'r', encoding='utf-8') as f:
        from_data = loader(f, **(from_args or {}))
    with open(to_path, 'r', encoding='utf-8') as f:
        to_data = loader(f, **(to_args or {}))
    to_data.update(from_data)

    with open(to_path, 'w', encoding='utf-8') as f:
        dumper(to_data, f, **(dump_args or {}))


def merge_json(from_path: str, to_path: str):
    _merge_file(
        from_path, to_path,
        json.load, json.dump,
        dump_args={'indent': 4}
    )


def merge_yaml(from_path: str, to_path: str):
    _merge_file(
        from_path, to_path,
        yaml.safe_load, yaml.safe_dump
    )


def merge_toml(from_path: str, to_path: str):
    _merge_file(
        from_path, to_path,
        toml.load, toml.dump
    )


def merge_options(from_path: str, to_path: str):
    _merge_file(
        from_path, to_path,
        options.load, options.dump,
        from_args={'remove_version': True},
    )


# Map of file patterns to merge functions
MERGE_MAP = {
    '**/*.json': merge_json,
    '**/*.json5': merge_json,
    '**/*.yaml': merge_yaml,
    '**/*.yml': merge_yaml,
    '**/*.toml': merge_toml,
    '**/options.txt': merge_options,
}
