import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# EL10 has no grsync package, so the role skips it there.

def is_el10(host):
    return (host.system_info.distribution in ('rocky', 'centos')
            and host.system_info.release.split('.')[0] == '10')


def test_grsync(host):
    if is_el10(host):
        assert not host.file('/usr/bin/grsync').exists
    else:
        f = host.file('/usr/bin/grsync')
        assert f.exists
        assert f.user == 'root'
