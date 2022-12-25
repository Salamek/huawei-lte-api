from setuptools import setup, find_packages


def read_readme() -> str:
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='huawei-lte-api',
    version='1.6.10',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'huawei_lte_api': ['py.typed']},
    install_requires=[
        'requests',
        'xmltodict',
        'pycryptodomex'
    ],
    tests_require=[
        'tox'
    ],
    url='https://github.com/Salamek/huawei-lte-api',
    license='LGPL-3.0 ',
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    description='API For huawei LAN/WAN LTE Modems',
    long_description=read_readme(),
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
    ],
    python_requires='>=3.6',
    project_urls={
        'Release notes': 'https://github.com/Salamek/huawei-lte-api/releases',
    },
)
