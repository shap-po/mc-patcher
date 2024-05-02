import unittest
from io import StringIO

from src.options import load, dump, KEY_CODES

test_new_options = '''
version:3120
autoJump:false
key_key.attack:key.mouse.left
key_key.use:key.mouse.right
key_key.forward:key.keyboard.w
key_key.left:key.keyboard.a
key_key.back:key.keyboard.s
key_key.right:key.keyboard.d
key_key.jump:key.keyboard.space
key_key.sneak:key.keyboard.left.control
key_key.sprint:key.keyboard.left.shift
key_key.drop:key.keyboard.q
key_key.inventory:key.keyboard.e
key_key.chat:key.keyboard.unknown
'''
test_old_options = '''
version:1343
autoJump:false
key_key.attack:-100
key_key.use:-99
key_key.forward:17
key_key.left:30
key_key.back:31
key_key.right:32
key_key.jump:57
key_key.sneak:29
key_key.sprint:42
key_key.drop:16
key_key.inventory:18
key_key.chat:0
'''
test_new_dict = {
    'version': 3120,
    'autoJump': False,
    'key_key.attack': 'key.mouse.left',
    'key_key.use': 'key.mouse.right',
    'key_key.forward': 'key.keyboard.w',
    'key_key.left': 'key.keyboard.a',
    'key_key.back': 'key.keyboard.s',
    'key_key.right': 'key.keyboard.d',
    'key_key.jump': 'key.keyboard.space',
    'key_key.sneak': 'key.keyboard.left.control',
    'key_key.sprint': 'key.keyboard.left.shift',
    'key_key.drop': 'key.keyboard.q',
    'key_key.inventory': 'key.keyboard.e',
    'key_key.chat': 'key.keyboard.unknown'
}
test_old_dict = {
    **test_new_dict,
    'version': 1343,
}


class TestOptions(unittest.TestCase):
    def test_load_new(self):
        self.assertEqual(load(StringIO(test_new_options)), test_new_dict)

    def test_load_old(self):
        self.assertEqual(load(StringIO(test_old_options)), test_old_dict)

    def test_load_versionless(self):
        new_dict = test_new_dict.copy()
        del new_dict['version']
        self.assertEqual(load(StringIO(test_new_options), remove_version=True), new_dict)

    def test_dump_new(self):
        self.assertEqual(dump(test_new_dict).strip(), test_new_options.strip())

    def test_dump_old(self):
        self.assertEqual(dump(test_old_dict).strip(), test_old_options.strip())
