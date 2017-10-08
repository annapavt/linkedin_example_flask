from setuptools import setup, find_packages

setup(
    name='linkedin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask'
    ],
)