import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_packer(host):
    assert host.run('packer -version').rc == 0


def test_vagrant(host):
    assert host.run('vagrant --version').rc == 0
