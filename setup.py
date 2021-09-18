"""
Setuptools based setup module
"""
from setuptools import setup, find_packages
import versioneer


setup(
    name='pyimapsync',
    version=versioneer.get_version(),
    description='Transfer emails between multiple IMAP servers.',
    url='https://github.com/jan-janssen/pysyncimap',
    author='Jan Janssen',
    author_email='jan.janssen@outlook.com',
    license='BSD',
    packages=find_packages(exclude=["*tests*"]),
    install_requires=[],
    cmdclass=versioneer.get_cmdclass(),
    entry_points={
        "console_scripts": [
            'pyimapsync=pyimapsync.__main__:command_line_parser'
        ]
    }
)