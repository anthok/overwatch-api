from setuptools import setup

__version__ = '0.5'

setup(
      name='overwatch-api',
      version=__version__,

      packages=['overwatch_api'],

      description='Overwatch API Wrapper using lootbox.eu',
      url='http://github.com/anthok/overwatch-api',
      author='Kyle Anthony <anthok>',
      license='MIT',
      install_requires=['aiohttp>=2.0.0',
                        'async_timeout'],
      test_suite='nose.collector',
      tests_require=['nose', 'vcrpy', 'asyncio'],
  )
