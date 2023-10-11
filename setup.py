from setuptools import setup
from setuptools import find_packages

setup(
    name='kargs',
    version='0.1.0',
    description='An argprase to/from Kconfig tool',
    url='https://github.com/fjullien/kargs',
    author='Franck Jullien',
    author_email='franck.jullien@collshade.fr',
    license='BSD 3-clause',
    packages=['kargs'],
    install_requires=['kconfiglib'],
    include_package_data=True,

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)
