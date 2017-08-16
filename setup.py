from setuptools import setup

setup(
    name='dartyo'
    , version='0.1'
    , py_modules=['dart']
    , install_requires=['click', 'termcolor', 'xmltodict']
    , entry_points='''
        [console_scripts]
        dartyo=dart:cli
    '''
)
