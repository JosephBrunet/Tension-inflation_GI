# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os.path

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()
    
    
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files(HERE+'/tension_inflation/resources')


print(extra_files)



setup(name='tension_inflation',
      version='1.0.0',
      description='Software controlling the tension-inflation device',
      long_description=README,  # Optional
      long_description_content_type='text/markdown',
      url='https://github.com/JosephBrunet/tension_inflation.git',
      author='Joseph Brunet',
      author_email='jo.brunet73@gmail.com',
      license='MIT',
      package_dir={'': 'tension_inflation'},
      packages=find_packages(where='tension_inflation'),
      package_data={'': extra_files},
      python_requires='>=3',
      install_requires=['PyQt5','pyserial','pyqtgraph','simple-pid','PIPython'],
      entry_points={
      'gui_scripts':['tension_inflation=tension_inflation.GUI_main:main',], 
      'console_scripts': ['tension_inflation_console=tension_inflation.GUI_main:main',],
      },
      )
