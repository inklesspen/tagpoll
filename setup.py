import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'Mako==0.9.0',
    'SQLAlchemy==0.8.2',
    'pyramid==1.4.5',
    'pyramid-mako==0.3',
    'pyramid-debugtoolbar==1.0.9',
    'zope.sqlalchemy==0.7.3',
    'transaction==1.4.1',
    'pyramid-tm==0.7',
    'waitress==0.8.7',
]

setup(name='tagpoll',
      version='0.1',
      description='tagpoll',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tagpoll',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = tagpoll:main
      [console_scripts]
      initialize_tagpoll_db = tagpoll.scripts.initializedb:main
      """,
      )
