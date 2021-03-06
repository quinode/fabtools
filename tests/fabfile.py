from fabric.api import *
from fabtools import icanhaz
import fabtools


def mysql():
    """
    Setup MySQL server, user and database
    """
    icanhaz.mysql.server(password='s3cr3t')

    with settings(mysql_user='root', mysql_password='s3cr3t'):

        icanhaz.mysql.user('myuser', 'foo')
        assert fabtools.mysql.user_exists('myuser')

        icanhaz.mysql.database('mydb', owner='myuser')
        assert fabtools.mysql.database_exists('mydb')


def postgresql():
    """
    Setup PostgreSQL server, user and database
    """
    icanhaz.postgres.server()

    icanhaz.postgres.user('pguser', 'foo')
    assert fabtools.postgres.user_exists('pguser')

    icanhaz.postgres.database('pgdb', 'pguser')
    assert fabtools.postgres.database_exists('pgdb')
