import pkgutil
import sys


def load_class(_class_name, _context):
    # dynamically load all available macop solutions
    loader = pkgutil.find_loader('macop.solutions.' + _class_name)
    _module = loader.load_module()
    _context['macop.solutions.' + _class_name] = _module
