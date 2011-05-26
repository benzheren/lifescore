import os
import sys

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
        password='',
        database='lifescore'
    ),
)

@task
def create_db_and_user():
    try:
        import MySQLdb
    except ImportError:
        print 'ERROR: please install MySQL-python lib first...'
    else:
        db = MySQLdb.connect(host=options.DB.host, user=options.DB.user,
                passwd=options.DB.password, db='')
        cursor = db.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS lifescore DEFAULT CHARACTER SET
                'utf8' DEFAULT COLLATE 'utf8_bin'""")
        cursor.execute("""GRANT ALL PRIVILEGES ON lifescore.* to
                'lifescore'@'localhost'""")
        cursor.execute("""SET PASSWORD FOR 'lifescore'@'localhost' = PASSWORD('5mad_cows')""")

@task
@needs('create_db_and_user')
def create_tables_from_sqlalchemy():
    try:
        import MySQLdb
    except ImportError:
        print 'ERRORL please install MySQL-python lib first...'
    else:
        from lifescore import models
        from sqlalchemy import create_engine
        engine = create_engine("mysql+mysqldb://lifescore:5mad_cows@localhost/" + 
                    "lifescore?charset=utf8&use_unicode=0")
        models.initialize_sql(engine)

@task
@needs('create_tables_from_sqlalchemy')
def load_data_sets():
    try:
        import MySQLdb
    except ImportError:
        print 'ERRORL please install MySQL-python lib first...'
    else:
        db = MySQLdb.connect(host=options.DB.host, user=options.DB.user,
                passwd=options.DB.password, db=options.DB.database)
        cursor = db.cursor()
        pass 

