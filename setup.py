from setuptools import setup

setup(name='crypto_analytics',
      version='0.0',
      # description='',
      url='http://github.com/Jacoab/crypto_analytics',
      # author='',
      # author_email='',
      # license='',
      packages=[
          'crypto_analytics',
          'crypto_analytics.collection',
          'crypto_analytics.collection.data_handler',
          'crypto_analytics.collection.data_source',
          'crypto_analytics.controller',
          'crypto_analytics.types',
          'crypto_analytics.types.symbol',
          'crypto_analytics.utils',
      ],
      install_requires=[
          'requests>=2.20.1',
          'pandas>=0.23.4 ',
          'numpy>=1.16.0',
      ],
      zip_safe=False)
