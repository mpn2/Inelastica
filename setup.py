#!/usr/bin/env python

import sys, time

# TODO: Compile F90helpers
# TODO: Check prerequireies
# TODO: Testcalculations

def test_prereq():

    try:
        import numpy as N
        import numpy.linalg as LA
    except:
        print "#### ERROR ####"
        print "Inelastica needs the package 'numpy' to run."
        print "Please see http://sourceforge.net/apps/mediawiki/inelastica/"
        print "#### ERROR ####"
        raise NameError('numpy package not found')

    try:
        import numpy.distutils
        import numpy.distutils.extension
    except:
        print "#### ERROR ####"
        print "Inelastica requires the f2py extension of numpy."
        print "Please see http://sourceforge.net/apps/mediawiki/inelastica/"
        print "#### ERROR ####"
        raise NameError('numpy f2py package not found')

    try:
        import netCDF4 as NC4
    except:
        print "#### ERROR ####"
        print "Inelastica requires netCDF4 (1.2.7 or newer recommended)"
        print "https://pypi.python.org/pypi/netCDF4"
        print "Please see http://sourceforge.net/apps/mediawiki/inelastica/"
        print "#### ERROR ####"
        raise NameError('netCDF4 package not found')

    # Make sure that numpy is compiled with optimized LAPACK/BLAS
    st = time.time()

    # For release 600!
    a = N.ones((600,600),N.complex)
    b = N.dot(a,a)
    c,d = LA.eigh(b)
    en = time.time()
    if en - st > 4.0:
        print "#### Warning ####"
        print "A minimal test showed that your system takes %3.2f s"%(en-st)
        print "numpy was compiled with a slow versions of BLAS/LAPACK."
        print "  (normal Xeon5430/ifort/mkl10 takes ~ 1 s)"
        print "Please see http://dipc.ehu.es/frederiksen/inelastica/index.php"
        print "#### Warning ####"

    try:
        import scipy
        import scipy.linalg as SLA
        import scipy.special as SS
    except:
        print "#### Warning ####"
        print 'Some modules will not work without the scipy package'
        print '(needed for solving generalized eigenvalue problems'
        print 'and spherical harmonics)'
        print "#### Warning ####"

test_prereq()

from numpy.distutils.core import setup
from numpy.distutils.system_info import get_info, NotFoundError
import numpy.distutils.extension as Next

# Fortran helper files
F90ext = Next.Extension('Inelastica.F90helpers',
                        ['package/F90/expansion_SE.f90',
                         'package/F90/readTSHS.f90',
                         'package/F90/removeUnitCellXij.f90',
                         'package/F90/setkpointhelper.f90'],
                        )

# Retrieve the LAPACK-library...
lapack_opt = get_info('lapack_opt')
if not lapack_opt:
    raise NotFoundError('No LAPACK/BLAS resources found')
F90extLapack = Next.Extension('Inelastica.F90_lapack',
                              ['package/F90/surfaceGreen.f90'],
                              **lapack_opt)

# Main setup of python modules
setup(name='Inelastica',
      version='1.2-rc',
      # Define the requirements for Inelastica
      # These probably needs to be adjusted... 
      requires = ['python (>=2.5)','numpy (>=1.6)','netCDF4 (>=1.2.7)'],
      description='Python tools for SIESTA/TranSIESTA', 
      long_description="""
Provides:
1:	File format conversions for geometry, try: geom2geom --help
2:	Phonon calculations (including e-ph coupling)
3:	Transmission calculations, try: pyTBT --help
4:	Eigenchannels analysis, try: EigenChannels --help
5:	IETS calculations, try: Inelastica --help
6:      grid2grid, try: grid2grid --help
7:	Scripts to set up the above type of calculations.""",
      author='Magnus Paulsson and Thomas Frederiksen', 
      author_email='magnus.paulsson@lnu.se / thomas_frederiksen@ehu.es',  
      url='https://sourceforge.net/apps/mediawiki/inelastica', 
      license='GPL. Please cite: Frederiksen et al., PRB 75, 205413 (2007)', 
      package_dir={'Inelastica': 'package'},
      scripts  = ['scripts/agr2pdf',
                  'scripts/Inelastica',
                  'scripts/EigenChannels',
                  'scripts/pyTBT',
                  'scripts/geom2geom',
                  'scripts/geom2zmat',
                  'scripts/Bandstructures',
                  'scripts/ElectronBands',
                  'scripts/ComputeDOS',
                  'scripts/siesta_cleanup',
                  'scripts/STMimage',
                  'scripts/Vasp2Siesta',
                  'scripts/bands2xmgr',
                  'scripts/Phonons',
                  'scripts/NEB',
                  'scripts/grid2grid',
                  'scripts/setupFCrun',
                  'scripts/setupOSrun',
                  'scripts/kaverage-TBT',
                  'scripts/WriteWavefunctions'
                  ],
      packages=['Inelastica'],
      ext_modules=[F90ext,F90extLapack],
      data_files=[('Inelastica/PBS', 
                   ['PBS/RUN.OS.pbs','PBS/RUN.py.pbs', 'PBS/RUN.TS.pbs']
                   )]
      )

