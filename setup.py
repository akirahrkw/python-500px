#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="python-500px",
      version="0.3.0",
      description="500PX API client",
      license="MIT",
      install_requires=["simplejson"],
      author="Akira Hirakawa",
      author_email="akirahrkw@gmail.com",
      url="https://github.com/akirahrkw/python-500px",
      packages = find_packages(),
      keywords= "500px",
      zip_safe = True)
