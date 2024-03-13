from setuptools import setup
from os.path import join, dirname

setup(
    name='dstt',
    version='0.1',
    packages=['dstt'],
    description='Damn Small/Simple Time Tracker',
    author='Vik Kotwizkiy',
    author_email='vik@vik.wtf',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['dstt = dstt.dstt:cli']
    },
    install_requires=[
        'fire==0.6.0'
    ],
    requires=['python (>= 3.6)'],
    license='WTFPL'
)
