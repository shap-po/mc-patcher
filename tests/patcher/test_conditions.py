import unittest
from src.patcher.conditions import *

from tests.utils import mock_dir

mocks = mock_dir({
    'root': {
        'instance1': {
            'mods': {
                'mod1': '',
                'mod2': '',
            }
        },
        'instance2': {
            'mods': {
                'mod2': '',
                'mod3': '',
            }
        },
        '_instance3': {
            'mods': {
                'mod3': '',
                'mod4': '',
            }
        },
        'folder': {
            'instance4': {
                'mods': {
                    'mod4': '',
                    'mod5': '',
                }
            }
        },
        'empty': {},
    }
})


class TestConditions(unittest.TestCase):
    @mocks
    def test_file_condition(self, *mocks):
        i1, i2, i3, i4 = GameInstance.from_path('root')

        instances = [
            {'mods': ['mods/mod1', 'mods/mod2'], 'instance': i1},
            {'mods': ['mods/mod2', 'mods/mod3'], 'instance': i2},
            {'mods': ['mods/mod3', 'mods/mod4'], 'instance': i3},
            {'mods': ['mods/mod4', 'mods/mod5'], 'instance': i4},
        ]
        mods = set()
        for instance in instances:
            mods.update(instance['mods'])

        self.assertTrue(FileConditionObject(file='mods/mod1').check(i1))

        # regular tests
        for instance in instances:
            for mod in instance['mods']:
                self.assertTrue(FileConditionObject(file=mod).check(instance['instance']))
            for mod in mods.difference(instance['mods']):
                self.assertFalse(FileConditionObject(file=mod).check(instance['instance']))

            # exists=False
            for mod in instance['mods']:
                self.assertFalse(FileConditionObject(file=mod, exists=False).check(instance['instance']))
            for mod in mods.difference(instance['mods']):
                self.assertTrue(FileConditionObject(file=mod, exists=False).check(instance['instance']))

        # multiple files
        for instance in instances:
            self.assertTrue(FileConditionObject(file=instance['mods']).check(instance['instance']))
            self.assertFalse(FileConditionObject(file=mods.difference(instance['mods'])).check(instance['instance']))

            # exists=False
            self.assertFalse(FileConditionObject(file=instance['mods'], exists=False).check(instance['instance']))
            self.assertTrue(FileConditionObject(file=mods.difference(
                instance['mods']), exists=False).check(instance['instance']))

        # multiple files (any)
        for instance in instances:
            self.assertTrue(FileConditionObject(
                file=[
                    instance['mods'][0],  # first mod exists
                    mods.difference(instance['mods'])  # all other mods don't exist
                ]
            ).check(instance['instance']))

        # glob pattern
        self.assertTrue(FileConditionObject(file='mods/mod*').check(i1))
        self.assertTrue(FileConditionObject(file='**/mod*').check(i1))

        self.assertFalse(FileConditionObject(file='not-mods/mod*').check(i1))

    @mocks
    def test_instance_condition(self, *mocks):
        instances = GameInstance.from_path('root')
        i1, i2, i3, i4 = instances

        # check basic path pattern
        self.assertTrue(InstanceConditionObject(instance_pattern='root/instance1').check(i1))
        self.assertFalse(InstanceConditionObject(instance_pattern='root/instance1').check(i2))

        self.assertTrue(InstanceConditionObject(instance_pattern='root/folder/instance4').check(i4))
        self.assertFalse(InstanceConditionObject(instance_pattern='root/instance4').check(i1))

        # check regex pattern
        for instance in (i1, i2):
            self.assertTrue(InstanceConditionObject(instance_pattern='root/instance[0-9]').check(instance))
        for instance in (i3, i4):
            # _instance3, folder/instance4
            self.assertFalse(InstanceConditionObject(instance_pattern='root/instance[0-9]').check(instance))

        for instance in instances:
            self.assertTrue(InstanceConditionObject(instance_pattern='root/.+').check(instance))

    def test_condition_factory(self, *mocks):
        file_conditions = [
            {'file': 'mods/mod1'},
            {'file': ['mods/mod1', 'mods/mod2']},
            {'file': 'mods/mod1', 'exists': False},
            {'file': ['mods/mod1', 'mods/mod2'], 'exists': False},
        ]
        for condition in file_conditions:
            self.assertIsInstance(BaseConditionObject.create_condition(condition), FileConditionObject)

        path_conditions = [
            {'instance_pattern': 'root/instance1'},
            {'instance_pattern': 'root/instance[0-9]'},
            {'instance_pattern': 'root/.+'},
        ]
        for condition in path_conditions:
            self.assertIsInstance(BaseConditionObject.create_condition(condition), InstanceConditionObject)
