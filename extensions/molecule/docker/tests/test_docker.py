import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# The test containers can't run a Docker daemon, so only the installation
# is checked.

def test_docker_packages(host):
    for p in ('docker-ce', 'docker-ce-cli', 'containerd.io',
              'docker-buildx-plugin', 'docker-compose-plugin'):
        assert host.package(p).is_installed


def test_docker_cli(host):
    assert host.run('docker --version').rc == 0
    assert host.run('docker compose version').rc == 0


def test_docker_access(host):
    assert 'docker' in host.user('user').groups


def test_docker_account(host):
    owner = host.run('getent passwd 1000 | cut -d: -f1').stdout.strip()
    if owner and owner != 'docker':
        # uid 1000 belongs to someone else, e.g. "ubuntu": no account
        assert not host.user('docker').exists
    else:
        docker = host.user('docker')
        assert docker.exists
        assert docker.uid == 1000
        assert docker.group == 'docker'
        assert docker.shell == '/usr/sbin/nologin'
        assert not host.file(docker.home).exists
