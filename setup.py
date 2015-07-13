from distutils.core import setup

setup(
    name='yomongo',
    version='0.1',
    packages=['yomongo'],
    url='',
    license='MIT',
    author='Trong Hieu HA',
    author_email='tronghieu.ha@gmail.com',
    description='A very lightweight Mongo ORM by using pymongo directly for request and Cerberus for validation',
    install_requires=[
        'Cerberus',
        'pymongo'
    ]
)