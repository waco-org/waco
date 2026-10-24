import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_rust_user(host):
    f = host.file('/home/user/.cargo/bin/rustc')
    assert f.exists
    assert f.user == 'user'
    assert f.group == 'user'


def test_installer_removed(host):
    assert host.run('ls /tmp/*rustup-init.sh').rc != 0
