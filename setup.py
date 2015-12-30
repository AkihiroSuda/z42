from distutils.core import setup
setup(
    name='z42',
    packages=['z42'],
    version='0.0.1',
    description='Zeroconf (mDNS) for Amazon EC2',
    author='Akihiro Suda',
    author_email='suda.kyoto@gmail.com',
    url='https://github.com/AkihiroSuda/z42',
    download_url='https://github.com/AkihiroSuda/z42/tarball/v0.0.1',
    license='Apache License 2.0',
    scripts=['bin/z42'],
    install_requires=[
        'boto3',
        'zeroconf'
    ],
    keywords=['zeroconf', 'mdns', 'ec2', 'dns'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Networking',
        'Topic :: Internet :: Name Service (DNS)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
