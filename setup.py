import sys
from setuptools import setup

if sys.version_info >= (3, 0):
    long_description = open('README.md', encoding='utf-8').read()
else:
    long_description = open('README.md').read()

setup(
    name='huawei-lte-api',
    version='1.0.15',
    packages=[
        'huawei_lte_api',
        'huawei_lte_api.api',
        'huawei_lte_api.enums',
        'huawei_lte_api.config'
    ],
    install_requires=[
        'requests',
        'dicttoxml',
        'xmltodict',
    ],
    url='https://github.com/Salamek/huawei-lte-api',
    license='LGPL-3.0 ',
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    description='API For huawei LAN/WAN LTE Modems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pylint',
        'pytest-cov'
    ]

)
