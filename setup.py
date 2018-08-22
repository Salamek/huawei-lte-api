from setuptools import setup

setup(
    name='huawei-lte-api',
    version='1.0',
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
    description='API For huawei LAN/WAN LTE Modems'
)
