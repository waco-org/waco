import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# Each component has its own scenario; this one checks that the workstation
# role applies them together, including the per-user settings.

def is_redhat(host):
    return host.system_info.distribution != 'ubuntu'


def test_user(host):
    assert host.user('user').exists


def test_system_package(host):
    assert host.file('/usr/bin/gvim').exists


def test_flatpak_system(host):
    if is_redhat(host):
        assert host.file('/var/lib/flatpak/app/org.musicbrainz.Picard').is_directory


def test_flatpak_user(host):
    if is_redhat(host):
        f = host.file('/home/user/.local/share/flatpak/app/org.freac.freac')
        assert f.is_directory
        assert f.user == 'user'


def test_docker_access(host):
    assert 'docker' in host.user('user').groups


def test_components(host):
    for command in ('docker --version', 'mvn --version', 'packer -version',
                    'vagrant --version', 'vboxmanage --version', 'code --version',
                    'uv --version'):
        assert host.run(command).rc == 0, command


def test_rust_user(host):
    f = host.file('/home/user/.cargo/bin/rustc')
    assert f.exists
    assert f.user == 'user'


def test_python_user(host):
    assert host.file('/home/user/.local/bin/python3.13').exists
    assert host.file('/home/user/.local/bin/tox').exists
