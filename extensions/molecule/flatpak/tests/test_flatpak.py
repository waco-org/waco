import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_flatpak_system(host):
    f = host.file('/var/lib/flatpak/app/org.musicbrainz.Picard')
    assert f.is_directory
    assert f.user == 'root'

