from setuptools import setup

setup(name='aws-tools',
      version='0.1',
      description='Tools for aws services',
      url='http://github.com/soda29/aws-tools',
      author='Nicolas Reynoso',
      author_email='nicolas.reynoso@headwaydigital.com',
      #license='MIT',
      packages=['aws_tools'],
      install_requires=[
          'boto3',
          'botocore'
      ],
      zip_safe=False)
