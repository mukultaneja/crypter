from setuptools import setup

setup(
    name='Crypter',
    version='0.1.0',
    py_modules=['Crypter'],
    install_requires=[
        'Click',
        'sqlalchemy'
    ],
    entry_points={
        'console_scripts': [
            'Crypter = crypter:cli',
        ],
    },
)