import pkgutil
from importlib import import_module


control_list = []

__path__ = pkgutil.extend_path(__path__, __name__)

for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
    if ispkg:
        continue

    module = import_module(modname)
    control_list.append(module)
