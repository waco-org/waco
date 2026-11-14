import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# Each component has its own scenario; this one checks that the workstation
# role applies them together.

def test_user(host):
    assert host.user('user').exists


def test_system_package(host):
    assert host.file('/usr/bin/gvim').exists


def test_flatpak_system(host):
    assert host.file('/var/lib/flatpak/app/org.musicbrainz.Picard').is_directory


def test_docker_access(host):
    assert 'docker' in host.user('user').groups


def test_user_entry(host):
    user = host.user('user')
    assert user.uid == 1001
    assert user.gid == 1001
    assert 'vboxusers' in user.groups
    admin = 'sudo' if host.system_info.distribution == 'ubuntu' else 'wheel'
    assert admin in user.groups


def test_docker_account(host):
    owner = host.run('getent passwd 1000 | cut -d: -f1').stdout.strip()
    if owner and owner != 'docker':
        assert not host.user('docker').exists
    else:
        assert host.user('docker').uid == 1000


def test_components(host):
    for command in ('docker --version', 'mvn --version', 'packer -version',
                    'vagrant --version', 'vboxmanage --version', 'uv --version'):
        assert host.run(command).rc == 0, command
    # code refuses to run as root
    assert host.file('/usr/bin/code').exists


# Java 21 is the default although 25 is newer, and stays so after Maven pulls
# in its own JDK; Maven runs on JAVA_HOME.
def test_java_default(host):
    assert 'version "21' in host.run('java -version').stderr
    assert host.check_output('javac -version').startswith('javac 21')
    assert 'Java version: 21' in host.check_output("bash -lc 'mvn --version'")


def test_system(host):
    config = host.run('systemd-analyze cat-config systemd/journald.conf').stdout
    assert 'Storage=persistent' in config
    assert '/usr/bin/true' in host.run('sudo -n -l -U user').stdout


def test_printing(host):
    assert host.run('lpstat -d').stdout.strip().endswith(': waco-test')
