__version__ = '0.1'

from nps.gateway import NPSGateway
gateway = NPSGateway()


__all__ = ['gateway', '__version__']
