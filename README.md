# Z42: Zeroconf (mDNS) for Amazon EC2

[![PyPI version](https://badge.fury.io/py/z42.svg)](http://badge.fury.io/py/z42)

In EC2, your public IP addresses can change intermittently.

Z42 allows you to resolve the IP addresses by their `Name` tags.

No DDNS required.

## Usage

    $ brew install awscli
    $ aws configure # enter your access key here
    $ pip3 install z42
    $ z42 &
	$ ssh ${YOUR_EC2_INST_NAME}.local

## Available Drivers

 * `z42.drivers.ec2.EC2Driver`: Amazon EC2

I welcome your pull requests for new drivers.
