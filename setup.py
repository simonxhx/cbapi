from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='cbapi',
    url='https://github.com/simonxhx/cbapi',
    author='Simon Xiong',
    author_email='simon.xiong.baruchmfe@gmail.com',
    # Needed to actually package something
    packages=['cbapi'],
    # Needed for dependencies
    install_requires=['json', 'requests', 'pandas', 'os', 'threading'],
    version='1.0.0',
    description='An API library for downloading organization and people data from Crunchbase',
    long_description=open('README.md').read(),
)
