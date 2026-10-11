waco_python
===========

![test](https://github.com/waco-org/waco-python/actions/workflows/test.yml/badge.svg)

An opinionated Ansible role that allows you to perform system and/or source Python installations and
to complement them by creating custom virtualenv's and installing Ansible, Mercurial or Sphinx.
Supported distributions are the currently maintained releases of the Red Hat family and
derivatives, and of the Ubuntu LTS variants. At this time tests are run on Rocky Linux 10, Rocky
Linux 9, CentOS Stream 10, CentOS Stream 9, Fedora 43, Fedora 42, Fedora 41, Ubuntu 24.04 and Ubuntu
22.04.


Requirements
------------

None.

Role Variables
--------------

The variables that control the role behaviour are listed below with their respective defaults:

    wapy_has_ansible: false

Whether to install Ansible. Ansible is installed in a specific virtualenv based on the most suitable
Python version: either source version compatible with the ``python3-libselinux`` package, if its
installation was requested, or the system's Python 3 installation.

    wapy_has_mercurial: false

Whether Mercurial should be installed. The latest available Python version will be used to create
a specific virtualenv.

    wapy_has_sphinx: false
    
Whether to install Sphinx, in a specific virtualenv based on the latest Python version available.

    wapy_user: python
    wapy_group: "{{ wapy_user }}"

Owner and group of source Python installations.

    wapy_source_versions: [ 3.13.1 ]

The Python source releases to be installed.

    wapy_build_root_dir: "/sw"

The base directory of the directory where source Python releases should be downloaded and built.

    wapy_install_root_dir: "/opt"
    
The base directory where Python releases should be installed.

    wapy_source_packages

A list of packages to be installed for each source Python release. See the ``defaults/main.yml``
file for the default list.

    wapy_source_venv: "dev"

Name of a custom virtualenv to be created.

    wapy_source_venv_root_dir: "/opt"

The base directory where virtualenv's based on source Python installations should be created.

    wapy_source_venv_prefix: "venv"

The prefix of the name of directories where all the virtualenv's for a specific Python installation
will be created. All virtualenv's for source Python x.y will be created in a ``venv-x.y``
directories.

    wapy_source_venv_packages:

A list of packages to install in the custom virtualenv. See the ``defaults/main.yml`` file for
the default list.

    wapy_system_venv_root_dir: "/opt"

The base directory where virtualenv's based on system Python installations should be created.

    wapy_system_venv_prefix: "sysvenv"

Directory name prefix for the directory of virtualenv's based on a specific system Python
installation.

    wapy_sphinx_venv: "doc"

The name of the Sphinx virtualenv.

    wapy_sphinx_packages:

The packages installed in the Sphinx virtualenv. See the ``defaults/main.yml`` file for the
default list.

Dependencies
------------

The ``nmusatti.source_python`` role is used to install Python from source.

The ``geerlingguy.repo-epel`` role is used to enable the EPEL repository on CentOS.

The ``bobbyrenwick.pip`` role is used to install pip.

Example Playbook
----------------

While it is certainly possible to use this role by itself, it is meant to be used in conjunction
with the [waco-master](https://github.com/waco-org/waco-master) role.

    - hosts: servers
      roles:
         - role: waco_org.waco_python
           vars:
             wapy_source_versions:
               - 3.13.1
             wapy_has_sphinx: true

License
-------

GPLv3

Author Information
------------------

Nicola Musatti - <https://github.com/nmusatti>

WACO - Workstation as Code - <https://github.com/waco-org>
