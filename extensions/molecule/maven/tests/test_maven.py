import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_maven(host):
    out = host.check_output('mvn --version')
    assert 'Apache Maven' in out


def test_maven_el9_stream(host):
    info = host.system_info
    if info.distribution in ('rocky', 'centos') and info.release.split('.')[0] == '9':
        assert 'Apache Maven 3.9' in host.check_output('mvn --version')


def test_no_upstream_maven(host):
    assert not host.file('/sw/maven').exists
