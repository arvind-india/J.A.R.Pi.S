
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='jarpis',
    version='0.0.1',
    description='J.A.R.Pi.S',
    long_description=readme,
    # author='Kenneth Reitz',
    # author_email='me@kennethreitz.com',
    # url='https://github.com/kennethreitz/samplemod',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)