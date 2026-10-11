import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_grsync(host):
    f = host.file('/usr/bin/grsync')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_maven(host):
    f = host.file('/opt/apache-maven-3.9.12/bin/mvn')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_packer(host):
    res = host.run('packer -version')

    assert res.rc == 0


def test_vagrant(host):
    res1 = host.run('vagrant --version')
    res2 = host.run('/opt/bin/vagrant --version')

    assert res1.rc == 0 or res2.rc == 0


def test_virtualbox(host):
    res = host.run('vboxmanage --version')

    assert res.rc == 0


def test_vscode(host):
    f = host.file('/usr/bin/code')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_rust_user(host):
    f = host.file('/home/user/.cargo/bin/rustc')

    assert f.exists
    assert f.user == 'user'
    assert f.group == 'user'
