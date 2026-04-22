import os
from pathlib import Path

from Cython.Build import cythonize
from setuptools import setup, Extension, Command

target_files = [
    'src/utils/*.py',
    'src/core/*.py',
    'src/routers/cookie/services.py',
    'src/routers/download/services.py',
    'src/routers/system/services.py',
    'src/routers/config/services.py',
]

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


class ClearFilesCommand(Command):
    description = '清理 build 目录和源码中的二进制文件 (.so/.pyd)'
    user_options = []

    def initialize_options(self): pass

    def finalize_options(self): pass

    def run(self):
        print("开始清理二进制文件...")

        for pattern in target_files:
            for file_path in Path().glob(pattern):
                parent_dir = file_path.parent
                base_name = file_path.stem

                for bin_file in parent_dir.glob(f"{base_name}.*"):
                    if bin_file.suffix in ['.so', '.pyd']:
                        os.remove(bin_file)
                        print(f"✓ 已移除二进制文件: {bin_file}")


setup(
    ext_modules = cythonize(
        make_extensions(target_files),
        exclude=["**/__init__.py"],
        build_dir="build/cython",      # 将生成的 .c 文件统一放入 build 目录，保持源码干净
        compiler_directives={
            'language_level': "3",     # 指定 Python 3
            'always_allow_keywords': True,
        },
    ),
    cmdclass={
        'clear_files': ClearFilesCommand,
    }
)
