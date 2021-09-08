from setuptools import setup, find_packages


setup(
    name='huawei-lte-api',
    version='1.4.18',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'huawei_lte_api': ['py.typed']},
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
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
    ],
    python_requires='>=3.4',
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pylint',
        'tox',
        'pytest-cov'
    ],
    project_urls={
        'Release notes': 'https://github.com/Salamek/huawei-lte-api/releases',
    },
)
