from setuptools import setup, find_packages
import os

version = '1.0'
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='openmultimedia.reporter',
      version=version,
      description="Citizen journalism for Plone.",
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='telesur reportero',
      author='Franco Pellegrini',
      author_email='frapell@ravvit.net',
      url='https://github.com/desarrollotv/openmultimedia.reporter',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['openmultimedia'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'httplib2',
        'Pillow',
        'Plone>=4.1',
        'borg.localrole',
        'plone.app.dexterity>=1.2.1',
        'plone.directives.dexterity>=1.0.2',
        'plone.formwidget.captcha',
        'plone.namedfile[blobs]',
        'collective.prettydate',
#we need to stay at the 1.8 version of collective.js.jqueryui for Plone 4.1
#https://github.com/collective/collective.js.jqueryui/issues/15
        'collective.js.jqueryui<1.9',
        'collective.z3cform.widgets',
        'openmultimedia.api',
        ],
      extras_require={
        'test': ['plone.app.testing',
                 'plone.app.caching',],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
