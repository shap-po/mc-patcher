import argparse

from src.patcher.config import Config
from src.instance import GameInstance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('instances', type=str,
                        help='Path to instances dir; can be multiple', nargs='+')
    parser.add_argument('--config', '-c', type=str, help='Path to config file')
    parser.add_argument('--data', '-d', type=str, help='Path to config data dir')
    parser.add_argument('--max-recursion', '-r', type=int, default=2, help='Max recursion depth')
    parser.add_argument('--preview', '-p', action='store_true', help='Preview the changes')

    args = parser.parse_args()

    print("[MC-PATCHER] Starting with args:", args)

    instances = []
    for instance in args.instances:
        instances.extend(GameInstance.from_path(instance, max_recursion=args.max_recursion))

    config = Config(
        config=args.config or 'configs/config.jsonc',
        config_files_dir=args.data or 'configs/',
    )

    has_changes = config.preview(instances)
    if not has_changes:
        print('[MC-PATCHER] No changes detected')
        return

    if args.preview:
        c = input('Apply changes? [y/n]: ')
        if c.lower() == 'y':
            config.apply(instances)
    else:
        config.apply(instances)


if __name__ == '__main__':
    main()
