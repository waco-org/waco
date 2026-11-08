import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def admin_group(host):
    return 'sudo' if host.system_info.distribution == 'ubuntu' else 'wheel'


def test_plain_name(host):
    alice = host.user('alice')
    assert alice.exists
    assert alice.uid >= 1000
    assert alice.group == 'alice'
    assert alice.shell == '/bin/bash'
    assert host.file(alice.home).is_directory


def test_full_entry(host):
    bob = host.user('bob')
    assert bob.uid == 1500
    assert bob.gid == 1600
    assert bob.group == 'bob'
    assert bob.gecos == 'Bob'
    assert bob.shell == '/bin/sh'
    assert admin_group(host) in bob.groups
    assert 'later' in bob.groups


def test_no_home(host):
    carol = host.user('carol')
    assert carol.exists
    assert not host.file(carol.home).exists
    assert 'adm' in carol.groups
    assert admin_group(host) not in carol.groups


def test_refusals(host):
    for marker in ('renumber', 'uid-taken', 'no-group'):
        assert host.file(f'/var/tmp/waco-users-{marker}').exists, marker
    assert host.user('alice').uid != 1777
    assert not host.user('dave').exists
