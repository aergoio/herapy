#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "base58",
    "ecdsa",
    "googleapis-common-protos",
    "protobuf",
    "cryptography",
    "toml",
    "grpcio",
]

setup_requirements = [
    'setuptools',
    'flake8',
    'wheel',
    'twine',
    'Sphinx',
    'sphinx_rtd_theme',
]

test_requirements = [
    'grpcio-tools',
    'pytest',
    'tox',
    'codecov',
    'pytest-cov',
    'pytest-mock',
]

setup(
    name='aergo-herapy',
    version='1.0.3',
    description="python SDK for AERGO",
    keywords='herapy',
    author="aergo.io",
    author_email='tech@aergo.io',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    packages=find_packages(include=['aergo']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aergoio/herapy',
    zip_safe=False,
)
