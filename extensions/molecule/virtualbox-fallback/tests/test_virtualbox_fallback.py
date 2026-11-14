import os
from pathlib import Path

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')

ROOT = Path(__file__).resolve().parents[4]
SHIPPED = ROOT / 'roles/virtualbox/files/oracle_vbox_2016.asc'
KEY_PATHS = ['/etc/apt/keyrings/virtualbox.asc', '/etc/pki/rpm-gpg/RPM-GPG-KEY-oracle-vbox-2016']


def test_virtualbox(host):
    assert host.run('vboxmanage --version').rc == 0


def test_downloaded_key_replaced_the_wrong_one(host):
    installed = [host.file(path) for path in KEY_PATHS if host.file(path).exists]
    assert len(installed) == 1
    assert installed[0].content_string.strip() == SHIPPED.read_text().strip()
