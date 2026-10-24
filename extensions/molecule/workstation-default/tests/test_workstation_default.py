import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def is_el(host):
    return host.system_info.distribution in ('rocky', 'centos')


def test_epel_and_crb(host):
    if is_el(host):
        assert host.package('epel-release').is_installed
        assert 'enabled' in host.check_output('/usr/bin/crb status')
        assert 'disabled' not in host.check_output('/usr/bin/crb status')


def test_apt_prerequisites(host):
    if host.system_info.distribution == 'ubuntu':
        assert host.package('python3-debian').is_installed
