from setuptools import setup

setup (name='clean_folder',
      version='0.0.1',
      package=['clean_folder'],
      author='Bodnia Serhii',
      entry_points={
          'console_scripts':['clean-folder = clean_folder.clean:main'],
    },
)