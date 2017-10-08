from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
download_url = 'https://github.com/codito/pyqtkeybind/tarball/' + __version__

setup(
    name='pyqtkeybind',
    version=__version__,
    description='Cross platform global keybindings for PyQt5',
    long_description=long_description,
    url='https://github.com/codito/pyqtkeybind',
    download_url=download_url,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Arun Mahapatra',
    install_requires=['xcffib', 'pyqt5'],
    author_email='arun@codito.in'
)
