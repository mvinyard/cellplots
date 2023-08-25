import setuptools
import re
import os
import sys

setuptools.setup(
    name="cellplots",
    version="0.0.0",
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard@broadinstitute.org",
    url="https://github.com/mvinyard/cellplots",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="Cell & Genomics Plotting",
    packages=setuptools.find_packages(),
    install_requires=[
        "matplotlib>=3.7.2",
        "pandas>=2.0.3",
	"ABCParse>=0.0.6",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
