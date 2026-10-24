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


def test_user_python(host):
    f = host.file('/home/user/.local/bin/python3.13')
    assert f.exists
    assert '3.13' in host.check_output('/home/user/.local/bin/python3.13 --version')


def test_user_tools(host):
    out = host.check_output('/home/user/.local/bin/tox --version')
    assert 'tox-uv' in out
    assert host.run('/home/user/.local/bin/ruff --version').rc == 0
