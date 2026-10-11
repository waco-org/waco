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


def test_docker_user(host):
    assert host.user("docker").exists
