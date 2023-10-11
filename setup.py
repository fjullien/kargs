from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='kargs',
    version='0.1.1',
    description='An argprase to/from Kconfig tool',
    url='https://github.com/fjullien/kargs',
    author='Franck Jullien',
    author_email='franck.jullien@collshade.fr',
    license='BSD 3-clause',
    packages=['kargs'],
    install_requires=['kconfiglib'],
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)
