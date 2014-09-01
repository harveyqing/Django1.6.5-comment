# Taken from Python 2.7 with permission from/by the original author.
import sys

from django.utils import six

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


if six.PY3:
    from importlib import import_module
else:
    def import_module(name, package=None):
        """Import a module.
        导入一个模块。

        The 'package' argument is required when performing a relative import. It
        specifies the package to use as the anchor point from which to resolve the
        relative import to an absolute import.
        当利用相对路径导入时，`package`参数是必须的。它指定包作为锚点使用，从这个锚点将相对导入
        解析为绝对导入。

        """
        if name.startswith('.'):  #: 以点`.`开头的是相对导入
            if not package:
                raise TypeError("relative imports require the 'package' argument")
            level = 0  #: 记录模块的层级，level = 0表示当前目录
            for character in name:
                if character != '.':  #: 遇到点号就表示层级加一
                    break
                level += 1
            name = _resolve_name(name[level:], package, level)
        __import__(name)  #: 绝对导入的话就直接用`__import__` builtin导入
        return sys.modules[name]
