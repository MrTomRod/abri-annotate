# based on https://realpython.com/pypi-publish-python-package
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setup(
    name='abri-annotate',
    version='0.0.2',
    description='Run ABRicate using multiple reference databases and maps the results onto genes',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/MrTomRod/abri-annotate',
    author='Thomas Roder',
    author_email='roder.thomas@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=['abri_annotate'],
    include_package_data=True,  # see MANIFEST.in
    install_requires=['fire', 'pandas', 'biopython'],
    entry_points={
        'console_scripts': [
            'abriannotate-bash=abri_annotate.ABRiannotateBash:main',
            'abriannotate-docker=abri_annotate.ABRiannotateDocker:main',
        ]
    },
)
