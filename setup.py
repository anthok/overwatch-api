from setuptools import setup

__version__ = '0.3'

setup(
      name='overwatch-api',
      version=__version__,

      packages=['overwatch_api'],

      description='Overwatch API Wrapper using lootbox.eu',
      url='http://github.com/anthok/overwatch-api',
      author='Kyle Anthony <anthok>',
      license='MIT',
      install_requires=['requests']
  )
