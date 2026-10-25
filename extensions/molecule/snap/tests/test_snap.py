import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# snap is Ubuntu only; on the Red Hat family the role must refuse to run.

def is_ubuntu(host):
    return host.system_info.distribution == 'ubuntu'


def test_snap(host):
    if is_ubuntu(host):
        assert host.file('/snap/bin/hello-world').exists
    else:
        assert not host.package('snapd').is_installed
