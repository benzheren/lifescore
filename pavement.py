import os
import sys

import MySQLdb
from paver.easy import *
import paver.doctools
from paver.setuputils import setup, find_package_data

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'repoze.tm2>=1.0b1', # default_commit_veto
    'zope.sqlalchemy',
    'WebError',
    'facebook-python-sdk',
    'python-memcached',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='lifescore',
      version='0.0',
      description='lifescore',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_package_data(),
      include_package_data=True,
      zip_safe=False,
      test_suite='lifescore',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = lifescore:main
      """,
      paster_plugins=['pyramid'],
      )

options(
    DB=Bunch(
        host='localhost',
        user='root',
        password=''
    ),
)

@task
def create_db_and_user():
    db = MySQLdb.connect(host=options.DB.host, user=options.DB.user,
            passwd=options.DB.password, db='')
    cursor = db.cursor()
    cursor.execute("""CREATE DATABASE IF NOT EXISTS lifescore DEFAULT CHARACTER SET
            'utf8' DEFAULT COLLATE 'utf8_bin'""")
    cursor.execute("""GRANT ALL PRIVILEGES ON lifescore.* to
            'lifescore'@'localhost'""")
    cursor.execute("""SET PASSWORD FOR 'lifescore'@'localhost' = PASSWORD('5mad_cows')""")

