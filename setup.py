from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksGdalCalc',
    version='0.0.1',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks gdal_calc.py library.',
    url='http://pypi.python.org/pypi/GeobricksGdalCalc/',
    keywords=['geobricks', 'gdal_calc', 'gis']
)
