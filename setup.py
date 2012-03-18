from setuptools import setup, find_packages
import os

version = '0.0.8'

try:
    # android
    from py4a import patch_distutils
    patch_distutils()
except: pass

setup(name='bit.bot.http',
      version=version,
      description="Bit Bot HTTP",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ryan Northey',
      author_email='ryan@3ca.org.uk',
      url='http://code.3ca.org.uk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bit', 'bit.bot'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
