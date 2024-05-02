import unittest
from tests.utils import mock_dir

from src.instance import GameInstance


mocks = mock_dir({
    'root': {
        'saves+mods': {
            'saves': {},
            'mods': {}
        },
        'mods': {
            'mods': {}
        },
        'saves': {
            'saves': {}
        },
        'empty': {
        },
        'instances': {
            'instance1': {
                'saves': {}
            },
        }
    }
})


class TestInstance(unittest.TestCase):
    @mocks
    def test_from_path(self, *mocks):
        instances = GameInstance.from_path('root', max_recursion=2)
        self.assertEqual(len(instances), 4)

        dirs = set(instance.path for instance in instances)
        self.assertEqual(dirs, {'root/saves+mods', 'root/mods',
                         'root/saves', 'root/instances/instance1'})

    @mocks
    def test_from_path_ignore(self, *mocks):
        instances = GameInstance.from_path('root', ignore=['saves+mods'], max_recursion=2)
        self.assertEqual(len(instances), 3)

        dirs = set(instance.path for instance in instances)
        self.assertEqual(dirs, {'root/mods', 'root/saves', 'root/instances/instance1'})

    @mocks
    def test_from_path_recursion(self, *mocks):
        instances = GameInstance.from_path('root', max_recursion=1)
        self.assertEqual(len(instances), 3)

        dirs = set(instance.path for instance in instances)
        self.assertEqual(dirs, {'root/saves+mods', 'root/mods', 'root/saves'})
