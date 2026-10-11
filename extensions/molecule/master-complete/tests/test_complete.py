import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def is_ubuntu(host):
    res = host.run('grep Ubuntu /etc/os-release')
    return res.rc == 0


def test_system_package(host):
    f = host.file('/usr/bin/gvim')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_flatpak_system(host):
    if not is_ubuntu(host):
        f = host.file('/var/lib/flatpak/app/org.musicbrainz.Picard')
        assert f.is_directory
        assert f.user == 'root'
        assert f.group == 'root'


def test_flatpak_user(host):
    if not is_ubuntu(host):
        f = host.file('/home/user/.local/share/flatpak/app/'
                      'org.freac.freac')
        assert f.is_directory
        assert f.user == 'user'
        assert f.group == 'user'
