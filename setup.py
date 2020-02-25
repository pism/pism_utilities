from distutils.core import setup

from batch_script import __version__

name = "pism_utilities"

setup(name=name,
      version=__version__,
      description="Python utilities for generating PISM's batch scripts",
      author='Andy Aschwanden and Constantine Khrulev',
      author_email='aaschwanden@alaska.edu',
      url='https://github.com/pism/pism_utilities',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities'
      ],
      packages=[name],
      package_dir={name: "."}
      )
