import argparse
import logging
import sys

import z42
from z42.core import Z42
from z42.drivers.ec2 import EC2Driver


def create_parser():
    parser = argparse.ArgumentParser(
        prog='z42',
        description='Z42: Zeroconf (mDNS) for EC2',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    drivers = ['ec2']
    parser.add_argument('-d', '--driver',
                        choices=drivers,
                        default='ec2',
                        help='driver (one of %s)' % drivers)
    parser.add_argument('-i', '--interval',
                        required=False,
                        type=int,
                        default=60 * 10,
                        help='interval in seconds')
    parser.add_argument('--debug',
                        action='store_true',
                        help='print debug-level logs')
    return parser


def create_z42(args):
    if args.driver != 'ec2':
        raise RuntimeError('Unknown driver  %s' % args.driver)
    driver = EC2Driver()
    z = Z42(driver, args.interval)
    return z


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.debug:
        z42.LOG.setLevel(logging.DEBUG)
    z = create_z42(args)
    z.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())
