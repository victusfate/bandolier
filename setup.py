from setuptools import setup
from setuptools import find_packages

setup(
  name='bandolier',
  version='0.1.0',
  description='yet another python utility library',
  url='https://github.com/victusfate/bandolier',
  author='victusfate',
  author_email='messel@gmail.com',
  license='MIT',
  packages=find_packages(),
  install_requires = [
    'boto3'
  ],
  # package_data={'bandolier': ['bandolier/*.json']},
  zip_safe=False
)
