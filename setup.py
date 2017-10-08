from setuptools import setup, find_packages
import io
import os


def read(*parts):
    """Reads the content of the file located at path created from *parts*."""
    try:
        return io.open(os.path.join(*parts), 'r', encoding='utf-8').read()
    except IOError:
        return ''


requirements = read('requirements', 'main.txt').splitlines()

setup(
    name='linkedin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)