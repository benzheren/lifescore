# LifeScore

## Development
### Local Environment Setup
Assume that you are using Mac OS X Snow Leopard (this means you will have python and related tools installed):

0. Install virtualenv and install [virtualenvwrapper](http://www.doughellmann.com/docs/virtualenvwrapper/). Use virtualenvwrapper tool to create virtual enviroment for Pyramid.
1. Install Mysql Community Server 5.1 64-bit or 32-bit from [here](http://dev.mysql.com/downloads/mysql/5.1.html).
2. Install [memcached](http://memcached.org/) by using [macports](http://www.macports.org/) or [HomeBrew](http://http://mxcl.github.com/homebrew/). HomeBrew is recommended.
3. Install RabbitMQ by following [this](http://docs.celeryproject.org/en/latest/getting-started/broker-installation.html#installing-rabbitmq-on-os-x). It should be very easy with HomeBrew. After installation, you need to start the server.
4. Install [`pip`](http://www.pip-installer.org/en/latest/installing.html) if you don't have it.
5. Then you can install all required library by running `pip install -r requirements.txt`
6. Initialize the mysql database by running `paver bootstrap`

### Run Application Locally
0. Start Celery by running command `celeryd -l info` under the project home folder
1. Start the app by `python setup.py develop && PYRAMID_DEBUG_ROUTEMATCH=true paster serve development.ini`

### Tips for MySQL import
* `mysqlimport -u root --fields-terminated-by=',' --fields-optionally-enclosed-by='"' --lines-terminated-by='\r\n' --verbose --columns=rank,name,city,short_name --local lifescore world_schools.csv`

