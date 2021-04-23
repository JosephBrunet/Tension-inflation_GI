# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(name='tension-inflation',
      version='1.0.0',
      description='Software controlling the tension-inflation device',
      long_description=long_description,  # Optional
      long_description_content_type='text/markdown',
      url='https://github.com/JosephBrunet/Tension-inflation_GI.git',
      author='Joseph Brunet',
      author_email='jo.brunet73@gmail.com',
      license='MIT',
      packages=find_packages(where='package'), 
      package_dir={
          '': 'package',
      },
      python_requires='>=3',
      install_requires=['pyqt','pyserial','pyqtgraph','simple-pid'],
      entry_points={  # Optional
        'console_scripts': [
            'tension-inflation=entry_point:main',
        ],
      },
      )
