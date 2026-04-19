from pathlib import Path

from Cython.Build import cythonize
from setuptools import setup, Extension


def make_extensions(path_patterns: list[str]):
    extensions = []

    for pattern in path_patterns:
        for file_path in Path().glob(pattern):
            if file_path.name == "__init__.py":
                continue

            if file_path.suffix != ".py":
                continue

            module_name = ".".join(file_path.with_suffix("").parts)
            extensions.append(Extension(module_name, [str(file_path)]))

    return extensions


target_files = make_extensions([
    'src/utils/*.py',
    'src/core/*.py',
    'src/routers/cookie/services.py',
    'src/routers/download/services.py',
    'src/routers/system/services.py',
])

setup(
    ext_modules = cythonize(
        target_files,
        exclude=["**/__init__.py"],
        build_dir="build/cython",      # 将生成的 .c 文件统一放入 build 目录，保持源码干净
        compiler_directives={
            'language_level': "3",     # 指定 Python 3
            'always_allow_keywords': True,
        },
    ),
)

# bash
# python setup.py build_ext --inplace
