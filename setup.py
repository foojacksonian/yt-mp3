from os import path
from codecs import open
from setuptools import setup, find_packages

long_description = "The ytmp3 program downloads, trims, encodes and tags songs acquired from YouTube."

setup(
    name='yt-mp3',
    version='0.1.0',
    description='Simple program to download, trim, encode and tag songs from Youtube.',
    long_description=long_description,
    url='https://github.com/foojacksonian/yt-mp3',
    author='Foo Jacksonian, Andrew Michaelis',
    author_email='amac@hyperplane.org',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7',
    keywords='music,mp3,YouTube',
    packages=find_packages(),
    scripts=['ytmp3.py'],
    install_requires=['pytube>=11.0.2', 'mutagen>=1.45.1']
)
