from setuptools import setup

with open('README', 'r') as f:
    long_description = f.read()

setup(
    name='parser',
    version='2.0',
    author='Bincha3000',
    author_email='bincha.1997@gmail.com',
    description='Verb finder moldule',
    long_description=long_description,
    license='MIT',
    packages=find_packages(),
    install_requires=['nltk',],
    url='https://github.com/Bincha3000/Directory-Parser'
)