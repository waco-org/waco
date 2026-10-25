import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# Each component has its own scenario; this one checks that the workstation
# role applies them together, including the per-user settings.

def is_ubuntu(host):
    return host.system_info.distribution == 'ubuntu'


def test_user(host):
    assert host.user('user').exists


def test_system_package(host):
    assert host.file('/usr/bin/gvim').exists


def test_flatpak_system(host):
    assert host.file('/var/lib/flatpak/app/org.musicbrainz.Picard').is_directory


def test_flatpak_user(host):
    f = host.file('/home/user/.local/share/flatpak/app/org.freac.freac')
    assert f.is_directory
    assert f.user == 'user'


# The apps scenario checks the catalog in full; here only that the
# workstation role passes waco_apps and the users' apps on.
def test_user_app(host):
    if is_ubuntu(host):
        assert host.package('nautilus-dropbox').is_installed
    else:
        assert host.file('/home/user/.local/share/flatpak/app/com.dropbox.Client').is_directory


def test_docker_access(host):
    assert 'docker' in host.user('user').groups


def test_components(host):
    for command in ('docker --version', 'mvn --version', 'packer -version',
                    'vagrant --version', 'vboxmanage --version', 'uv --version'):
        assert host.run(command).rc == 0, command
    # code refuses to run as root
    assert host.file('/usr/bin/code').exists


def test_rust_user(host):
    f = host.file('/home/user/.cargo/bin/rustc')
    assert f.exists
    assert f.user == 'user'


def test_python_user(host):
    assert host.file('/home/user/.local/bin/python3.13').exists
    assert host.file('/home/user/.local/bin/tox').exists
