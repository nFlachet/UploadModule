from setuptools import setup

setup(name='UploadModule',
      version='0.1.0',
      packages=['UploadModule'],
      entry_points={
          'console_scripts': [
              'UploadModule = FileHandlerService.UploadForm.__main__:main'
          ]
      },
      )
