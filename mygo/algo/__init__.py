import os
import importlib

module_dir = os.path.dirname(__file__)

for filename in os.listdir(module_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        importlib.import_module(f".{module_name}", package=__name__)
