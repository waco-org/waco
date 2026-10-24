import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_vscode(host):
    f = host.file('/usr/bin/code')
    assert f.exists
    assert f.user == 'root'


def test_single_apt_source(host):
    if host.system_info.distribution == 'ubuntu':
        out = host.check_output(
            'grep -rl packages.microsoft.com/repos/code /etc/apt/sources.list.d || true')
        assert len(out.split()) == 1, out
