from __future__ import unicode_literals

import os
import re
import setuptools


version = (
    re
    .compile(r".*__version__ = '(.*?)'", re.S)
    .match(open('bob/__init__.py').read())
    .group(1)
)

packages = [
    str(s) for s in
    setuptools.find_packages('.', exclude=('tests', 'tests.*'))
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyaml>=14.0.0,<15.0.0',
    'thed>=0.1.5,<0.2',
    'click>=2.0.0,<3.0.0',
    'depot>=0.0.12,<0.1',
    'boto>=2.3.0,<2.4',
    'hipchat',
    'configobj',
    'pilo>=0.3.8,<0.4',
    'semantic_version>=2.3.0,<2.4',
    'gevent'
]

extras_require = {
    'tests': [
        'blumpkin>=0.4.0,<0.5.0',
        'ipdb',
        'webtest',
    ]
}

scripts = [
    'bin/bob',
]


setuptools.setup(
    name='bobb',
    version=version,
    description='bob the builder',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Balanced',
    author_email='dev+bob@balancedpayments.com',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    scripts=scripts,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    test_suite='nose.collector',
    dependency_links=[
        'http://github.com/tagged/python-hipchat/tarball/master#egg=hipchat'
    ]

)
