import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_dropbox(host):
    if host.system_info.distribution == 'ubuntu':
        assert host.package('nautilus-dropbox').is_installed
    else:
        assert host.file('/var/lib/flatpak/app/com.dropbox.Client').is_directory
