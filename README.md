# MC Patcher

A collection of patches for Minecraft instances. It allows you to apply patches to the instance files before launching the game. The patches are defined in a JSON file and can be used to copy, symlink, merge, or overwrite files in the instance folder based on conditions.

It's recommended to use the [Prism Launcher](https://prismlauncher.org/download/) as it allows running the script before launching the game.

# Config example

```jsonc
{
    "patches": [
        {
            "patch": {
                // can be a list of files with different methods
                "file": "options.txt", // from the root of the instance
                "with": "data/options.txt", // from the configs folder
                "method": "insert" // overwrite | insert | symlink | merge
            },
            "if": {
                "file": "options.txt",
                "exists": false
            }
            // reads as: if options.txt does not exist in the instance, get it from the configs folder
        },
        {
            "patch": {
                "file": "config/ias.json",
                "with": "data/ias.json",
                "method": "symlink"
            },
            "if": [
                // must match all conditions, if we want to match any, we can use "or" inside the object with the same structure
                {
                    "file": "config/ias.json",
                    "exists": false
                },
                {
                    "file": ["mods/InGameAccountSwitcher*.jar", "mods/In-Game Account Switcher*.jar"], // match any variant of the mod file
                    "exists": true
                }
            ]
            // reads as: if ias.json does not exist in the game config folder and in-game account switcher mod is installed, symlink ias.json from the configs folder
        }
    ]
}

```
# Usage

## Install

1. Clone the repository
2. Have Python 3.8+ installed
3. Create and activate a virtual environment
    Windows:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
    Linux:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
4. Install the requirements
    ```bash
    pip install -r requirements.txt
    ```
5. Copy the `config.example.jsonc` to `config.jsonc` and edit it to your needs

## Running

In Prism Launcher, navigate to **Settings** -> **Custom Commands** -> **Pre-launch command:**

Windows:
```bash
path_to_mc_patcher/run.bat $INST_DIR
```
Linux:
```bash
path_to_mc_patcher/run.sh $INST_DIR
```

Now, Prism will automatically run the script before launching the game, with $INST_DIR replaced with the launched instance directory.
