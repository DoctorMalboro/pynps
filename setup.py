# esto es para python 3
import os
import re

from setuptools import setup

def find_packages(library_name):
    """
    Compatibility wrapper.

    Taken from storm setup.py.
    """
    try:
        from setuptools import find_packages
        return find_packages()
    except ImportError:
        pass
    packages = []
    for directory, subdirectories, files in os.walk(library_name):
        if "__init__.py" in files:
            packages.append(directory.replace(os.sep, "."))
    return packages

v_file = open(os.path.join(os.path.dirname(__file__),
                        'nps', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(v_file.read()).group(1)

display_name = "nps"
library_name = "nps"
version = VERSION
description = "Library to work with NPS payment gateway."
authors = "Emiliano Dalla Verde Marcozzi"
authors_email = "edvm@fedoraproject.org"
license = "LICENSE"
url = "https://github.com/edvm/pynps"

setup(
    name=display_name,
    version=version,
    author=authors,
    author_email=authors_email,
    description=description,
    url=url,
    license=license,
    packages=find_packages(library_name),
    install_requires=['suds-jurko',],
    entry_points={
        'console_scripts':
            []
            },
    )
