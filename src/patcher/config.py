from src.instance import GameInstance

# file handlers
import json5 as json

from src.patcher.patch import PatchObject, PatchHandler


class Config:
    def __init__(self, config: dict | str, config_files_dir: str):
        if isinstance(config, str):
            with open(config, 'r') as f:
                config = json.load(f)

        self.patches = [PatchHandler.from_dict(patch_data)
                        for patch_data in config.get('patches', [])]
        PatchObject.CONFIG_FILES_DIR = config_files_dir

    def apply(self, instances: list[GameInstance]):
        for instance in instances:
            for patch in self.patches:
                patch.apply(instance)

    def preview(self, instances: list[GameInstance]):
        has_changes = False
        for instance in instances:
            patches: list[PatchObject] = []
            for patch in self.patches:
                patches.extend(patch.preview(instance))

            if not patches:
                continue
            for patch in patches:
                print(f'Instance: {instance.path}')
                print(f'  {patch.file} -> {patch.with_file} ({patch.method})')
                has_changes = True

        return has_changes
