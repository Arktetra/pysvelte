from pathlib import Path

PYSVELTE_ROOT = Path(__file__).parents[2].absolute()
SRC = PYSVELTE_ROOT / "pkg"
DIST = PYSVELTE_ROOT / "dist"
PACKAGE_JSON = PYSVELTE_ROOT / "package.json"
NODE_MODULES = PYSVELTE_ROOT / "node_modules"

def set_root(path: Path | str):
    global PYSVELTE_ROOT
    path = path if isinstance(path, Path) else Path(str)
    PYSVELTE_ROOT = path