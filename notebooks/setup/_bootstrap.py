from __future__ import annotations

import sys
from pathlib import Path


def setup_project_path() -> Path:
    project_root = Path(__file__).resolve().parents[2]
    src_path = project_root / "src"
    src_str = str(src_path)
    if src_str in sys.path:
        sys.path.remove(src_str)
    sys.path.insert(0, src_str)

    stale_modules = [
        name
        for name in list(sys.modules)
        if name == "embedding_retrieval" or name.startswith("embedding_retrieval.")
    ]
    for name in stale_modules:
        sys.modules.pop(name, None)

    from embedding_retrieval.config import load_env

    load_env(project_root)

    try:
        from IPython import get_ipython
        ipy = get_ipython()
        if ipy is not None:
            ipy.run_line_magic("load_ext", "autoreload")
            ipy.run_line_magic("autoreload", "2")
    except Exception:
        pass

    return project_root
