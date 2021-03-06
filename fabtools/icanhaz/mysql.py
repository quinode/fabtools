"""
Idempotent API for managing MySQL users and databases
"""
from fabtools.mysql import *
from fabtools.deb import is_installed, preseed_package
from fabtools.icanhaz.deb import package
from fabtools.icanhaz.service import started


def server(version='5.1', password=None):
    """
    I can haz MySQL server
    """
    if not is_installed("mysql-server-%s" % version):
        if password is None:
            password = prompt_password()

        with settings(hide('running')):
            preseed_package('mysql-server', {
                'mysql-server/root_password': ('password', password),
                'mysql-server/root_password_again': ('password', password),
            })

        package('mysql-server-%s' % version)

    started('mysql')


def user(name, password, **kwargs):
    """
    I can haz MySQL user
    """
    if not user_exists(name, **kwargs):
        create_user(name, password, **kwargs)


def database(name, **kwargs):
    """
    I can haz MySQL database
    """
    if not database_exists(name, **kwargs):
        create_database(name, **kwargs)
