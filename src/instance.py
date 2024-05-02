import os


class GameInstance:
    def __init__(self, path: str):
        self.path = path

    @classmethod
    def from_path(cls, path: str, ignore: list[str] = None, max_recursion: int = 2) -> list['GameInstance']:
        instances = []

        # reached the maximum recursion depth
        if max_recursion == 0:
            return instances

        for folder in os.listdir(path):
            # ignore files
            wd = os.path.join(path, folder)
            if not os.path.isdir(wd):
                continue

            # ignore the folders in the ignore list
            if ignore and folder in ignore:
                continue

            # check if the folder is an instance
            # try both saves and mods folders because new instances can only have one of them
            if os.path.isdir(os.path.join(wd, 'saves')) or os.path.isdir(os.path.join(wd, 'mods')):
                instances.append(cls(wd))
            else:
                # if not, check the subfolders
                instances.extend(cls.from_path(wd, ignore, max_recursion - 1))

        return instances
