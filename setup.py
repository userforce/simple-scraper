from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scraperex',
    version='0.0.3',
    description='Web scraper using dynamic proxy and user agent.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/userforce/scraper',
    author='Tudor Corcimar',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='scraper proxy user-agent',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.7',
    install_requires=['re','requests','collections','fake_useragent']
)