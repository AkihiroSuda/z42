import logging
import socket
import sys
import zeroconf


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s (at %(filename)s:%(lineno)d)')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class Util:

    @classmethod
    def pretty(cls, x):
        if isinstance(x, zeroconf.ServiceInfo):
            try:
                srv = x.server
                addr = socket.inet_ntoa(x.address)
                return '<ServiceInfo server=%s, address=%s>' % (srv, addr)
            except Exception:
                return str(x)
        else:
            return str(x)
