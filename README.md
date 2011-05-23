# LifeScore

## Development
### Local Environment Setup
Assume that you are using Mac OS X Snow Leopard (this means you will have python and related tools installed):

0. Install virtualenv and install [virtualenvwrapper](http://www.doughellmann.com/docs/virtualenvwrapper/). Use virtualenvwrapper tool to create virtual enviroment for Pyramid.
1. Install Mysql Community Server 5.1 64-bit or 32-bit from [here](http://dev.mysql.com/downloads/mysql/5.1.html).
2. Install [memcached](http://memcached.org/) by using [macports](http://www.macports.org/) or [HomeBrew](http://http://mxcl.github.com/homebrew/). HomeBrew is recommended.
3. Install [`pip`](http://www.pip-installer.org/en/latest/installing.html) if you don't have it.
4. Then you can install all required library by running `pip install -r requirements.txt`
5. Initialize the mysql database by running `paver create_db_and_user`

