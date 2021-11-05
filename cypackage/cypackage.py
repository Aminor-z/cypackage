import argparse
import os
from subprocess import Popen
import begin
try:
    import easycython  # <- you need this
except:
    print("I need the package called 'easycython'.")
    exit(-1)


def get_package(package):
    import importlib
    try:
        m = importlib.import_module(package)
        return m.__path__[0]
    except:
        try:
            m = importlib.import_module(package)
            return m.__path__
        except:
            return None


@begin.start
def main(*package, remove_cython=False, not_clear=False, annotation=True, numpy_includes=True, debugmode=False):
    easycython_extra_args = f'{" --annotation " if annotation else " --no-annotation "}{" --numpy-includes " if numpy_includes else " --no-numpy-includes "}{" --debugmode " if debugmode else " --no-debugmode "}'
    dirname: str = str()
    if len(package) == 0:
        _package = (input('Please input the top package or package path: '))
    else:
        _package = package[0]
    if os.path.exists(_package):
        dirname = os.path.abspath(_package)
    else:
        p = get_package(_package)
        if p is None:
            print(f"I can't find this package or package path: {_package}")
            exit(-1)
        else:
            dirname = p
    py_files = []
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if file.endswith(".py"):
                if file != "__init__.py":
                    py_files.append(os.path.join(root, file))
            elif file.endswith(".c"):
                os.remove(os.path.join(root, file))
    for file in py_files:
        if remove_cython:
            os.remove(file)
        else:
            cwd = os.path.abspath(os.path.dirname(file))
            f = os.path.basename(file)
            print(f"easycython {f} {easycython_extra_args}")
            p = Popen(f"easycython {f} {easycython_extra_args}", cwd=cwd)
            p.wait(20)
            if not not_clear:
                try:
                    os.remove(os.path.splitext(file)[0] + '.html')
                    os.remove(os.path.splitext(file)[0] + '.c')
                except:
                    pass
    print("============finish============")
