import os
from setuptools import setup, find_packages



setup(
    name='pybigcommerce',
    version='0.1.0',

    packages=find_packages(),
    install_requires=['requests>=2.20.0'],

    url='https://github.com/bigcommerce/bigcommerce-api-python',
    download_url='https://pypi.python.org/packages/source/b/bigcommerce/bigcommerce-{}.tar.gz'.format(VERSION),

    author='Jamessen.Liu',
    author_email='liumaosen121@gmail.com',

    description='Using Python to connect Bigcommerce API',
    license='MIT',

    keywords=['bigcommerce', 'api'],
    classifiers=[
        'Development Status :: 3 - alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)