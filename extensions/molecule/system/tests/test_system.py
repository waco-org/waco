import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_mdns(host):
    if host.exists('firewall-cmd'):
        assert host.run('firewall-cmd --query-service=mdns').rc == 0
        assert host.run('firewall-cmd --permanent --query-service=mdns').rc == 0
    else:
        # The role doesn't install a firewall
        assert host.system_info.distribution == 'ubuntu'


def test_journal(host):
    config = host.run('systemd-analyze cat-config systemd/journald.conf').stdout
    assert 'Storage=persistent' in config
    assert 'SystemMaxUse=200M' in config
    assert host.service('systemd-journald').is_running
    assert host.file('/var/log/journal').is_directory


def test_sudoers(host):
    f = host.file('/etc/sudoers.d/waco-user-true')
    assert f.user == 'root' and f.mode == 0o440
    assert '/usr/bin/true' in host.run('sudo -n -l -U user').stdout
    assert not host.file('/etc/sudoers.d/waco-old').exists
    assert host.file('/etc/sudoers.d/local').exists


def test_broken_sudoers_refused(host):
    assert host.file('/var/tmp/waco-sudoers-broken').exists
    assert not host.file('/etc/sudoers.d/waco-broken').exists
    assert host.run('visudo -c').rc == 0
