waco_master
===========

![test](https://github.com/waco-org/waco-master/actions/workflows/test.yml/badge.svg)

An Ansible role that orchestrates the installation of several developer oriented tools by driving
other roles. Supported distributions are the currently maintained releases of the Red Hat family and
derivatives, and of the Ubuntu LTS variants. At this time tests are run on Rocky Linux 10, Rocky
Linux 9, CentOS Stream 10, CentOS Stream 9, Fedora 43, Fedora 42, Fedora 41, Ubuntu 24.04 and
Ubuntu 22.04.

The currently supported tools and applications are:

- Docker Community Edition
- Python, from either source or system packages, and within virtualenv's:

    + Ansible
    + Mercurial
    + Sphinx

- Flatpak and flatpak applications, both system and user level (Red Hat family only)
- Grsync
- Apache Maven
- Hashicorp Packer
- Hashicorp Vagrant
- Oracle VirtualBox
- Visual Studio Code
- Rust, per user

Requirements
------------

None.

Role Variables
--------------

There are many variables that control the operation of this role, they are documented in the
[defaults/main.yml](https:defaults/main.yml) file.

Dependencies
------------

The `nmusatti.docker_ce` role is used to install Docker Community Edition.

The `nmusatti.source_python` role is used to install Python from source.

The `waco_org.waco_python` is used to customize Python installations.

The `geerlingguy.repo-epel` role is used to enable the EPEL repository on CentOS.

The `bobbyrenwick.pip` role is used to install pip.

Example Playbook
----------------

Consider using the [waco-bootstrap](https://github.com/waco-org/waco-bootstrap.git) project to apply
the `waco-master` role to newly installed computers. Otherwise you can invoke it directly, in
which case you might want to copy and customize the `defaults/main.yml` file, and pass it as a
variable file:

    - hosts: servers
      roles:
         - role: waco_org.waco_master
           vars_file: my_defaults.yml

License
-------

GPLv3

Author Information
------------------

Nicola Musatti - <https://github.com/nmusatti>

WACO - Workstation as Code - <https://github.com/waco-org>
