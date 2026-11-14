import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_uv(host):
    assert host.run('uv --version').rc == 0


def test_no_source_builds(host):
    assert host.run('ls -d /opt/Python-* /opt/venv-*').rc != 0
    assert not host.user('python').exists

