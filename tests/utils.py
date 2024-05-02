import fnmatch
import typing
from unittest import mock

import os
from io import StringIO


class Mocks:
    """
    Holds multiple mocks. Can be used as a decorator to apply all mocks to a function.

    Example:
    ```
    mocks = Mocks(mock1=mock1, mock2=mock2)

    # apply single mock by it's name
    @mocks.mock1
    def test_function():
        ...

    # apply all mocks
    @mocks
    def test_function():
        ...
    ```
    """

    def __init__(self, **mocks):
        self.mocks = mocks

    def __getattr__(self, item):
        return self.mocks[item]

    def __getitem__(self, item):
        return self.mocks[item]

    def __call__(self, func):
        for mock in self.mocks.values():
            func = mock(func)
        return func


class File:
    '''Holds the content of a file.'''

    def __init__(self, content: str):
        self.content = content

    def get_io(self):
        '''Returns a StringIO that mocks the file.'''
        io = StringIO(self.content)
        default_close = io.close  # save the original close method

        def close():  # override the close method to save the content before closing
            self.content = io.getvalue()
            default_close()
        io.close = close

        return io


MockDir = typing.Dict[str, typing.Union[str, 'MockDir']]


def mock_dir(obj: MockDir) -> Mocks:
    """
    Creates mocks for
    - os.listdir
    - os.path.isdir
    - os.path.isfile
    - os.path.join
    - os.path.exists
    - os.walk
    - glob.glob
    - open
    with the given dictionary.

    :param obj: A dictionary containing the directories and files to mock.
    Example:
        {'root': {'file1': 'content1', 'folder1': {'file2': 'content2'}}}
    Will create mocks for the following paths:
    - root/
    - root/file1 with content 'content1'
    - root/folder1/
    - root/folder1/file2 with content 'content2'

    :return: A `Mocks` object containing the mocks.  
    """

    # replace all files in the dictionary with File objects
    def replace_files(obj):
        for key, value in obj.items():
            if isinstance(value, dict):
                replace_files(value)
            else:
                obj[key] = File(value)

    replace_files(obj)

    def get(path: str):
        '''Returns the object at the given path or None if it doesn't exist.'''
        path = path.replace('\\', '/').strip('/')
        current = obj
        for folder in path.split('/'):
            if folder not in current:
                return None
            current = current[folder]
        return current

    def get_all(_obj: MockDir) -> list[str]:
        '''Returns a list of all paths inside the object.'''
        items = []
        for item, content in _obj.items():
            items.append(item)
            if isinstance(content, dict):
                items.extend(f'{item}/{subitem}' for subitem in get_all(content))
        return items

    mock_listdir = mock.patch('os.listdir', side_effect=lambda path: list(get(path).keys()))
    mock_isdir = mock.patch('os.path.isdir', side_effect=lambda path: isinstance(get(path), dict))
    mock_isfile = mock.patch('os.path.isfile', side_effect=lambda path: not isinstance(get(path), dict))
    default_join = os.path.join
    mock_join = mock.patch('os.path.join', side_effect=lambda *args: default_join(*args).replace('\\', '/'))
    mock_exists = mock.patch('os.path.exists', side_effect=lambda path: get(path) is not None)

    def mock_walk_effect(path: str):
        current = get(path)
        if not isinstance(current, dict):
            return
        yield path, list(current.keys()), []

        for folder, content in current.items():
            if isinstance(content, dict):
                yield from mock_walk_effect(f'{path}/{folder}')
    mock_walk = mock.patch('os.walk', side_effect=mock_walk_effect)

    def mock_glob_effect(pathname: str, root_dir: str = None):
        dirs = get_all(obj)
        if root_dir is None:
            return fnmatch.filter(dirs, pathname)

        root_dir = root_dir.replace('\\', '/').strip('/')
        matches = []
        for dirname in dirs:
            if not dirname.startswith(root_dir):
                continue
            dirname = dirname[len(root_dir):].lstrip('/')
            if fnmatch.fnmatch(dirname, pathname):
                matches.append(dirname)
        return matches
    mock_glob = mock.patch('glob.glob', side_effect=mock_glob_effect)

    def mock_open_effect(path: str, *args, **kwargs):
        file = get(path)
        if file is None:
            raise FileNotFoundError(f'No such file or directory: {path}')
        return file.get_io()  # return a StringIO object that mocks the file
    mock_open = mock.patch('builtins.open', side_effect=mock_open_effect)

    return Mocks(
        os_path_listdir=mock_listdir,
        os_path_isdir=mock_isdir,
        os_path_isfile=mock_isfile,
        os_path_join=mock_join,
        os_path_exists=mock_exists,
        os_walk=mock_walk,
        glob_glob=mock_glob,
        open=mock_open,
    )
