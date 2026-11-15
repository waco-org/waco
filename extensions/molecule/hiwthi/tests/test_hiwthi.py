import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


@pytest.mark.parametrize('command', ['age --version', 'mise --version', 'uv --version'])
def test_tools(host, command):
    assert host.run(command).rc == 0


def test_no_hiwthi_yet(host):
    assert not host.file('/usr/local/bin/hiwthi').exists
