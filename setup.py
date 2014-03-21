from setuptools import setup, find_packages

setup(
    name="py-neorm4j",
    version="0.0.1",

    description='A basic ORM for Neo4j',
    long_description=open('README.md').read(),
    author='Kyle Valade',
    author_email='kylevalade@gmail.com',
    keywords='python, neo4j',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=['neo4jrestclient==2.0.0'],
    packages=find_packages(),
    include_package_data=True,
)
