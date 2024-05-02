import os
import glob
import re

from src.instance import GameInstance


class BaseConditionObject:
    def __init__(self, *args, **kwargs):
        pass  # TODO: implement "or" field for conditions

    def check(self, instance: GameInstance) -> bool:
        return self._check(instance)

    def _check(self, instance: GameInstance) -> bool:
        raise NotImplementedError

    @staticmethod
    def create_condition(condition_data: dict):
        if 'file' in condition_data:
            return FileConditionObject(**condition_data)
        if 'instance_pattern' in condition_data:
            return InstanceConditionObject(**condition_data)

        raise NotImplementedError(f'Unknown condition type: {condition_data}')


class FileConditionObject(BaseConditionObject):
    def __init__(self, file: str | list[str], exists: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = [file] if isinstance(file, str) else file
        self.exists = exists

    @staticmethod
    def _check_file(base_path: str, file: str, exists: bool) -> bool:
        return (glob.glob(file, root_dir=base_path) != []) == exists

    def _check(self, instance: GameInstance) -> bool:
        return any(self._check_file(instance.path, file, self.exists) for file in self.file)


class InstanceConditionObject(BaseConditionObject):
    def __init__(self, instance_pattern: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_pattern = re.compile(instance_pattern)

    def _check(self, instance: GameInstance) -> bool:
        return self.instance_pattern.match(instance.path.replace('\\', '/')) is not None
