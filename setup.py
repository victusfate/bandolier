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
    'boto3==1.13.*',
    'requests>=2.22.0,<3.0.0',
    'requests-oauthlib>=1.3.0,<2.0.0'
  ],
  # package_data={'bandolier': ['bandolier/*.json']},
  zip_safe=False
)
