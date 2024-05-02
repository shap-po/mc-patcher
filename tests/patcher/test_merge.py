import unittest
from src.patcher.merge import *

from tests.utils import mock_dir

data1 = {'a': 1, 'b': 2}
data2 = {'b': 3, 'c': 4}

data_merged = {'a': 1, 'b': 3, 'c': 4}

mocks = mock_dir({
    'root': {
        'json': {
            'data1.json': json.dumps(data1),
            'data2.json': json.dumps(data2),
        },
        'yaml': {
            'data1.yaml': yaml.dump(data1),
            'data2.yaml': yaml.dump(data2),
        },
        'toml': {
            'data1.toml': toml.dumps(data1),
            'data2.toml': toml.dumps(data2),
        },
        'options': {
            '1': {
                'options.txt': options.dump(data1),
            },
            '2': {
                'options.txt': options.dump(data2),
            },
        }
    }
})


tests = [
    ('root/json/data2.json', 'root/json/data1.json', merge_json, json.load),
    ('root/yaml/data2.yaml', 'root/yaml/data1.yaml', merge_yaml, yaml.safe_load),
    ('root/toml/data2.toml', 'root/toml/data1.toml', merge_toml, toml.load),
    ('root/options/2/options.txt', 'root/options/1/options.txt', merge_options, options.load),
]


def test_merge(path1: str, path2: str, merger, loader):
    merger(path1, path2)
    with open(path2, 'r', encoding='utf-8') as f:
        data = loader(f)
    return data


class TestMerge(unittest.TestCase):
    @mocks
    def test_loaders(self, *mocks):
        for path1, path2, merger, loader in tests:
            data = test_merge(path1, path2, merger, loader)
            self.assertEqual(data, data_merged)

    @mocks
    def test_auto_merge(self, *mocks):
        for path1, path2, merger, loader in tests:
            data = test_merge(path1, path2, merge, loader)
            self.assertEqual(data, data_merged)
