import stat
import subprocess
import threading
from pathlib import Path

from pysvelte import config


def mtime(path: Path):
    """
    Returns modification time of path.
    """
    try:
        st = path.stat()
    except FileNotFoundError:
        return 0

    if stat.S_ISDIR(st.st_mode):
        fs = list(path.rglob("*"))
        
        if fs:
            return max(mtime(f) for f in fs)
        else:
            return 0
    else:
        return st.st_mtime
    
def is_npm_install_necessary():
    """
    Check if npm dependencies are out of date or missing.
    """
    if not config.NODE_MODULES.exists():
        return True
    return mtime(config.NODE_MODULES) < mtime(config.PACKAGE_JSON)
    
def install_if_necessary():
    """
    Install npm modules if they're out of date or missing.
    """
    if is_npm_install_necessary():
        print("Running npm install...")
        subprocess.check_call(["npm", "--prefix", str(config.PYSVELTE_ROOT), "install"])

vis_build_lock = threading.Lock()

def build_if_necessary(paths=None):
    with vis_build_lock:
        dists = [config.DIST / p for p in paths] or [config.DIST]
        stale = any(
            mtime(dist) < mtime(config.SRC) or mtime(dist) < mtime(config.PACKAGE_JSON)
            for dist in dists
        )
        
        if stale:
            print("pysvelte components appear to be unbuilt or stale")
            install_if_necessary()
            print("Building pysvelte components with vite...")
            subprocess.check_call(["node", "build.ts"], cwd=str(config.PYSVELTE_ROOT))
        
def get_component_path(name):
    return config.SRC / f"{name}.svelte"

def get_script_tag(path: Path):
    build_if_necessary([path])
    with open(config.DIST / path, "r") as stream:
        tag = stream.read()
    return f"<script>{tag}</script>"