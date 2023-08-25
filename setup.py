import setuptools
import re
import os
import sys

setuptools.setup(
    name="getzlab-pyplots",
    version="0.0.0",
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard@broadinstitute.org",
    url="https://github.com/mvinyard/getzlab-pyplots",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="A possible plotting assistant and resource for members of the Getz Lab.",
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
