# -*- coding: utf-8 *-*

import re
import string

from datetime import date
from datetime import datetime

from weakref import WeakKeyDictionary


VALIDATE_EMAIL = re.compile(  # thanks django
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)

VALIDATE_URL = re.compile(r"""\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""", re.IGNORECASE)

VALIDATE_VERSION = re.compile(r'[0-9]\.[0-9]')

class Text(object):
    """ Tipo de datos base para los fields de tipo Text

        Parametros opcionales al crear una instancia:
            - length(int) = Longitud exacta que debe tener el string.
            - min_length(int) = Longitud minima que debe tener el string.
            - max_length(int) = Longitud maxima que debe tener el string.
            - null(bool) = Si se permite un string como cadena vacia '',
                           por defecto no se permite.
            - in_(iterable) = Lista, tupla o algún iterable con elementos
                              permitidos. Si el valor que se recibe como
                              parametro no se encuentra en este iterable
                              se arroja una excepción. Util para cuando
                              una variable solo puede tomar un valor de
                              entre una lista de valores.
            - default(value) = Valor por defecto para el campo.
            - accept_invalid_values(bool) No respetar las validaciones asignada
                                          al tipo de dato. Por defcto es False.
    """

    def __init__(self, length=None, min_length=None, max_length=None,
                 null=False, in_=None, default=None,
                 accept_invalid_values=False):

        self.data = WeakKeyDictionary()

        self.in_ = in_
        self.null = null
        self.length = length
        self.default = default
        self.min_length = min_length
        self.max_length = max_length
        self.accept_invalid_values = accept_invalid_values

        if default:
            self.value = self._validate(default)

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        self.data[instance] = self._validate(value)

    def _validate(self, value):
        """ Validacion para los tipos Text
        """

        vlength = len(value)
        exc = None

        if vlength == 0 and not self.null:
            exc = ValueError('Argument cant be \'\'')
        if self.length:
            if vlength != self.length:
                msg = 'Argument must have exactly length %s' % self.length
                exc = ValueError(msg)
        if self.max_length:
            if vlength > self.max_length:
                msg = 'Value cant be bigger than %s' % self.max_length
                exc = ValueError(msg)
        if self.min_length:
            if vlength < self.min_length:
                msg = 'Value cant be small than %s' % self.min_length
                exc = ValueError(msg)
        if self.in_:
            if value not in self.in_:
                msg = 'Value must be one of %s' % repr(self.in_)
                exc = ValueError(msg)

        if exc and not self.accept_invalid_values:
            raise exc

        return value


class Email(object):

    _value = None

    def __init__(self, validate=False):
        self.validate = validate

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, name, value):
        if self.validate:
            if not bool(VALIDATE_EMAIL.match(value)):
                raise ValueError()
        self._value = value


class Version(object):

    _value = None

    def __init__(self, validate=False):
        self.validate = validate

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, name, value):
        if self.validate and value is not None:
            if not bool(VALIDATE_VERSION.match(str(value))):
                raise ValueError('Invalid version')
        self._value = value


class Url(object):

    _value = None

    def __init__(self, validate=True, max_length=255):
        self.validate = validate
        self.max_length = max_length

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, name, value):
        if self.validate and value is not None:
            if not bool(VALIDATE_URL.match(value)):
                raise ValueError('Invalid URL Format')
        if len(value) > self.max_length:
            msg = 'Url cant be longer than %s chars' % self.max_length
            raise ValueError(msg)
        self._value = value


class Date(object):

    _value = None

    def __init__(self, today=False):
        self.today = today

    def __get__(self, instance, owner):
        if self.today:
            self.__set__('_value', date.today())
        return self._value

    def __set__(self, name, value):
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        if not isinstance(value, date):
            msg = 'Argument must be a datetime date instance'
            raise ValueError(msg)
        self._value = value.strftime('%Y-%m-%d')


class DateTime(object):

    _value = None

    def __init__(self, now=False):
        self.now = now

    def __get__(self, instance, owner):
        if self.now:
            self.__set__('_value', datetime.now())
        return self._value

    def __set__(self, name, value):
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if not  isinstance(value, datetime):
            msg = 'Argument must be a datetime instance'
            raise ValueError(msg)
        self._value = value.strftime('%Y-%m-%d %H:%M:%S')


class Time(DateTime):

    def __set__(self, name, value):
        if isinstance(value, str):
            value = datetime.strptime(value, '%H:%M:%S')
        if not isinstance(value, datetime):
            msg = 'Argument must be a datetime instance'
            raise ValueError(msg)
        self._value = value.strftime('%H:%M:%S')


class MD5(object):

    _value = None
    MD5_LENGTH = 32

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, name, value):
        if not self.is_md5(value):
            msg = 'Argument must be a valid md5 hash'
            raise ValueError(msg)
        self._value = value

    def is_md5(self, value):
        if not all(c in string.hexdigits for c in value):
            return False
        if len(value) != self.MD5_LENGTH:
            return False
        return True


class Numeric(Text):
    """ Caracteres númericos en el rango del 0 al 9. El valor del caracter
    numerico debe ser pasado como string, por ej: '032' o '12'
    """

    def __set__(self, name, value):
        if not value.isdigit():
            msg = 'Argument must be numbers but passed as strings, like "132"'
            raise ValueError(msg)
        super(Numeric, self).__set__(name, value)


class Amount(Text):
    """Representa un importe expresado en la menor denominación de la
    moneda. En Argentina, esto son centavos. Ej: $150.32 son 15032 ctvs."""

    def __set__(self, name, value):
        value = value.replace(',', '').replace('.', '')
        if not value.isdigit():
            msg = 'Argument must be numbers but passed as strings, like "132"'
            raise ValueError(msg)
        super(Amount, self).__set__(name, value)


class Alfa(Text):
    """ Solo caracteres alfabéticos, en el rango de la 'A' a la 'Z' y de la
    'a' a la 'z'.
    """

    set_ = '^[a-zA-Z]+$'
    exc_ = 'Only values with ASCII letters accepted'

    def __set__(self, name, value):
        expr = re.compile(self.set_)
        if not bool(expr.match(value)):
            raise ValueError(self.exc_)
        super(Alfa, self).__set__(name, value)

class Alfanumeric(Alfa):
    """ Alfa + Numeric. Cualquier caracter que sea un número del 0 al 9, una
    letra de la 'a' a la 'z' o de la 'A' a la 'Z'.
    """

    set_ = '^[a-zA-Z0-9]+$'
    exc_ = 'Only Alfa and Numeric chars are allowed'


class Order(Alfa):
    """ Alfanumeric + '_' + '-' + '.'
    """

    set_ = '^[a-zA-Z0-9 \_\-\.]+$'
    exc_ = 'Only Alfa, Numeric, "_", "-" and "." chars are allowed'


class MerchantId(Alfa):
    """ Alfanumeric + '_'
    """

    set_ = '^[a-zA-Z0-9 \_]+$'
    exc_ = 'Only Alfa, Numeric, and "_" chars are allowed'


class Country(Text):
    """ Paises según ISO 3166_1.
    """

    set_ = '^[A-Z]{3}$'
    exc_ = 'Only country codes according to the ISO 3166-1 are allowed'
