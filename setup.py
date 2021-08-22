from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='loglib',
    version='1.2.1',
    description='A decent logging system with some settings built in',
    url='https://github.com/teddybear315/loglib',
    author='Logan Houston',
    author_email='logan.houston4509@gmail.com',
    license='Free Domain',
    packages=['loglib'],
    install_requires=['neotermcolor>=2.0'],
    classifiers=[
        'Programming Language :: Python :: 3.9'
    ],
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown'
)
