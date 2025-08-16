import os
import glob
from os.path import dirname, isfile


def __list_all_modules():
    work_dir = dirname(__file__)
    mod_paths = glob.glob(os.path.join(work_dir, "*", "*.py"))

    all_modules = []
    for f in mod_paths:
        if isfile(f) and f.endswith('.py') and not f.endswith('__init__.py'):
            # rel: 'tools\logo.py' or 'mics/notes.py'
            rel = os.path.relpath(f, work_dir)
            mod = os.path.splitext(rel)[0].replace(os.path.sep, '.')
            # return module name fragment like '.tools.logo' so concatenation
            # 'Audify.plugins' + m -> 'Audify.plugins.tools.logo'
            all_modules.append('.' + mod)

    return sorted(all_modules)


ALL_MODULES = __list_all_modules()
__all__ = ALL_MODULES + ['ALL_MODULES']
