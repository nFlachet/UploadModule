from setuptools import setup

setup(name='UploadModule',
      version='0.1.0',
      packages=['UploadModule'],
      entry_points={
          'console_scripts': [
              'UploadModule = UploadModule.__main__:main'
          ]
      },
      )