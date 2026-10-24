import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# Flatpak is only supported on the Red Hat family for now.

def is_redhat(host):
    return host.system_info.distribution != 'ubuntu'


def test_flatpak_system(host):
    if is_redhat(host):
        f = host.file('/var/lib/flatpak/app/org.musicbrainz.Picard')
        assert f.is_directory
        assert f.user == 'root'


def test_flatpak_user(host):
    if is_redhat(host):
        f = host.file('/home/user/.local/share/flatpak/app/org.freac.freac')
        assert f.is_directory
        assert f.user == 'user'
        assert f.group == 'user'


def test_no_flatpak_elsewhere(host):
    if not is_redhat(host):
        assert not host.package('flatpak').is_installed
