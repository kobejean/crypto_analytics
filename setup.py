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
          'crypto_analytics.types',
          'crypto_analytics.utils',
      ],
      zip_safe=False)
