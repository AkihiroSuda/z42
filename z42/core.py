import time
import zeroconf

import z42
import z42.common
import z42.driver

LOG = z42.LOG.getChild(__name__)


class Z42(object):

    def __init__(self, driver, interval):
        assert isinstance(driver, z42.driver.Driver)
        assert isinstance(interval, int)
        assert interval > 0
        self.driver = driver
        self.interval = interval
        self.zc = zeroconf.Zeroconf()
        self.services = []

    def run(self):
        LOG.info('Starting Z42 (driver: %s, interval: %d seconds)',
                 self.driver, self.interval)
        try:
            self.loop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            LOG.exception(e)
        finally:
            LOG.info('Exiting..')
            self.unregister_all_services()
            self.zc.close()

    def register_service(self, srv):
        LOG.info('Registering %s', z42.common.Util.pretty(srv))
        self.zc.register_service(srv)

    def unregister_service(self, srv):
        LOG.info('Unregistering %s', z42.common.Util.pretty(srv))
        self.zc.unregister_service(srv)

    def register_all_services(self):
        for srv in self.driver.get_service_infos():
            assert isinstance(srv, zeroconf.ServiceInfo)
            self.register_service(srv)
            self.services.append(srv)

    def unregister_all_services(self):
        for srv in self.services:
            self.unregister_service(srv)
        self.services = []

    def loop(self):
        # TODO: watch events from driver
        while True:
            self.register_all_services()
            time.sleep(self.interval)
            self.unregister_all_services()
