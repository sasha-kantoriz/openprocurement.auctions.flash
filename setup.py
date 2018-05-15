from setuptools import setup, find_packages
import os

version = '1.0.6'

entry_points = {
    'openprocurement.auctions.core.plugins': [
        'auctions.flash = openprocurement.auctions.flash.includeme:includeme'
    ],
    'openprocurement.auctions.flash.plugins': [
        'flash.migration = openprocurement.auctions.flash.migration:migrate_data'
    ],
    'openprocurement.tests': [
        'auctions.flash = openprocurement.auctions.flash.tests.main:suite'
    ]
}

requirements = [
    'setuptools',
    'openprocurement.auctions.core',
    'openprocurement.schemas.dgf',
    'schematics-flexible'
]

test_requirements = requirements + []

setup(name='openprocurement.auctions.flash',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/openprocurement/openprocurement.auctions.flash',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.auctions'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      extras_require={'test': test_requirements},
      entry_points=entry_points,
      )
