import enum
import os
import shutil

from src.instance import GameInstance
from src.patcher.conditions import BaseConditionObject, FileConditionObject
from src.patcher.merge import merge


class Method(enum.Enum):
    OVERWRITE = 'overwrite'
    INSERT = 'insert'
    SYMLINK = 'symlink'

    MERGE = 'merge'


class PatchObject:
    CONFIG_FILES_DIR: str

    def __init__(self, file: str, with_file: str, method: str | Method):
        self.file = file
        self.with_file = with_file
        self.method = Method(method) if isinstance(method, str) else method

    def apply(self, instance: GameInstance):
        os.makedirs(os.path.join(instance.path, os.path.dirname(self.file)), exist_ok=True)

        from_path = os.path.join(self.CONFIG_FILES_DIR, self.with_file)
        to_path = os.path.join(instance.path, self.file)

        if self.method == Method.OVERWRITE:
            self._overwrite(from_path, to_path)
        elif self.method == Method.INSERT:
            self._insert(from_path, to_path)
        elif self.method == Method.SYMLINK:
            self._symlink(from_path, to_path)
        elif self.method == Method.MERGE:
            merge(from_path, to_path)
        else:
            raise NotImplementedError(f'Unknown method: {self.method}')

    def _overwrite(self, from_path: str, to_path: str):
        if os.path.exists(to_path):
            os.remove(to_path)
        shutil.copyfile(from_path, to_path)

    def _insert(self, from_path: str, to_path: str):
        if os.path.exists(to_path):
            return
        shutil.copyfile(from_path, to_path)

    def _symlink(self, from_path: str, to_path: str):
        if os.path.exists(to_path):
            os.remove(to_path)
        if os.path.islink(to_path):
            os.unlink(to_path)
        if os.path.isdir(from_path):
            os.symlink(from_path, to_path, target_is_directory=True)
        else:
            os.symlink(from_path, to_path)


class PatchHandler:
    def __init__(self, patches: list[PatchObject], conditions: list[FileConditionObject]):
        self.patches = patches
        self.conditions = conditions

    @classmethod
    def from_dict(cls, patch_data: dict):
        patch_objs = []
        condition_objs = []

        # get patch data
        p = patch_data.get('patch')
        if p:
            # wrap in list if not already
            p = [p] if isinstance(p, dict) else p
            # convert each patch to PatchObject
            for patch in p:
                patch['with_file'] = patch['with']
                del patch['with']
                patch_objs.append(PatchObject(**patch))

        # same for conditions
        c = patch_data.get('if')
        if c:
            c = [c] if isinstance(c, dict) else c
            for condition in c:
                condition_objs.append(BaseConditionObject.create_condition(condition))

        return cls(patch_objs, condition_objs)

    def apply(self, instance: GameInstance):
        if all(condition.check(instance) for condition in self.conditions):
            for patch in self.patches:
                patch.apply(instance)

    def preview(self, instance: GameInstance):
        patches: list[PatchObject] = []
        if all(condition.check(instance) for condition in self.conditions):
            for patch in self.patches:
                patches.append(patch)

        return patches
