"""
Fabric tools for managing Python packages using pip
"""
from distutils.version import StrictVersion as V
from fabric.api import *
from fabric.utils import puts


def is_pip_installed(version=None):
    """
    Check if pip is installed
    """
    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
        res = run('pip --version')
        if version is None:
            return res.succeeded
        else:
            installed = res.split(' ')[1]
            if V(installed) < V(version):
                puts("pip %s found (version >= %s required)" % (installed, version))
                return False
            else:
                return True


def install_pip():
    """
    Install pip
    """
    with cd("/tmp"):
        run("curl --silent -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py")
        sudo("python get-pip.py")


def is_installed(package, virtualenv=None):
    """
    Check if a Python package is installed
    """
    options = []
    if virtualenv:
        options.append('--environment="%s"' % virtualenv)
    options = " ".join(options)
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("pip freeze %(options)s" % locals())
    packages = [line.split('==')[0] for line in res.splitlines()]
    return (package in packages)


def install(packages, upgrade=False, virtualenv=None, use_mirrors=True, use_sudo=False):
    """
    Install Python packages
    """
    func = use_sudo and sudo or run
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = []
    if virtualenv:
        options.append('--environment="%s"' % virtualenv)
    if use_mirrors:
        options.append('--use-mirrors')
    if upgrade:
        options.append("--upgrade")
    options = " ".join(options)
    func('pip install %(options)s %(packages)s' % locals())
