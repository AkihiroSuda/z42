import boto3
import socket
import zeroconf

import z42
import z42.common
import z42.driver

LOG = z42.LOG.getChild(__name__)


class EC2Driver(z42.driver.Driver):

    def __init__(self):
        try:
            self.region_names = self.fetch_region_names()
            LOG.debug('Available region names: %s', self.region_names)
        except Exception as e:
            raise RuntimeError(
                'Could not fetch region names. This error is likely to happen when you did not run `aws configure`.', e)

    def fetch_region_names(self):
        ec2c = boto3.client('ec2')
        names = [f['RegionName'] for f in ec2c.describe_regions()['Regions']]
        return names

    def get_service_info_for_instance(self, inst):
        ip = inst.public_ip_address
        hostname = None
        try:
            hostname = [f['Value'] for f in inst.tags if f['Key'] == 'Name'][0]
        except (IndexError, TypeError):
            LOG.warning('No "Name" tag is assigned for %s. Using %s as the name.',
                        inst.id, inst.id)
            hostname = inst.id
        # TODO: sanitize name!
        assert isinstance(hostname, str), '%s is not string?' % hostname

        desc = {'model': 'Z42 (driver: %s)' % __name__}
        srv = zeroconf.ServiceInfo(
            type='_device-info._tcp.local.',
            name='%s._device-info._tcp.local.' % hostname,
            address=socket.inet_aton(ip),
            port=0,
            weight=0,
            priority=0,
            properties=desc,
            server='%s.local.' % hostname)
        return srv

    def get_service_infos_for_region(self, region_name):
        LOG.debug('Scanning %s', region_name)
        ec2r = boto3.resource('ec2', region_name=region_name)
        insts = ec2r.instances.all()
        for inst in insts:
            try:
                srv = self.get_service_info_for_instance(inst)
                LOG.debug('Found %s (%s) on %s',
                          z42.common.Util.pretty(srv),
                          inst, region_name)
                yield srv
            except Exception as e:
                LOG.warning('Could not get information for %s on %s: %s',
                            inst, region_name, e)
                LOG.exception(e)

    # overrides Driver
    def get_service_infos(self):
        for region in self.region_names:
            for srv in self.get_service_infos_for_region(region):
                yield srv
