# -*- coding: utf-8 -*-

import os
import yaml


class Dict2Object(object):
    """Dado un diccionario como constructor, cuando se pide un atributo
    de la instancia de esta clase, se retorna el valor asociado a la key
    del diccionario pasado al constructor."""

    def __init__(self, obj):
        assert isinstance(obj, dict), 'Argument must be a dict instance.'
        self._data = dict()
        for kw in obj:
            newobj = obj[kw]
            if isinstance(newobj, dict):
                self._data[kw] = Dict2Object(newobj)
            else:
                self._data[kw] = newobj

    def __getattr__(self, name):
        return self._data.get(name, None)


class Config(dict):
    """Configuration helper class.

    It starts empty, and then the config can be set at any time.
    """

    def __init__(self, file_=None):
        """Constructor arguments:
               file_: Path to a yaml config file.
        """
        if file_:
            self.load_file(file_)

    def load_file(self, filename):
        """Set the configuration from a YAML file."""
        with open(filename, "rt") as fh:
            cfg = yaml.load(fh.read())
        self.update(cfg)


confdir = os.path.join('/etc/pynps')
if os.getuid():
    confdir = os.path.expanduser('~/.config/pynps')
settings = Dict2Object(Config(os.path.join(confdir, 'pynps.yaml')))
