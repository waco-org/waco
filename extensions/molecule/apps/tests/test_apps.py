import json
import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# The same assertions on every distro: each app is checked as the catalog
# says, and the catalog says where it is unavailable.

USER_HOME = '/home/user'

COMMAND_DIRS = ['/var/lib/flatpak/exports/bin', '/snap/bin',
                USER_HOME + '/.local/share/flatpak/exports/bin']

DESKTOP_DIRS = ['/usr/share/applications',
                '/var/lib/flatpak/exports/share/applications',
                '/var/lib/snapd/desktop/applications',
                USER_HOME + '/.local/share/flatpak/exports/share/applications']


def resolved(host, scope):
    return json.loads(host.file(f'/var/tmp/waco-apps-{scope}.json').content_string)


def is_installed(host, check):
    if 'command' in check:
        name = check['command']
        return host.exists(name) or any(
            host.file(f'{d}/{name}').exists for d in COMMAND_DIRS)
    if 'desktop' in check:
        return any(host.file(f"{d}/{check['desktop']}.desktop").exists
                   for d in DESKTOP_DIRS)
    raise ValueError(f'unknown check {check}')


@pytest.mark.parametrize('scope', ['system', 'user'])
def test_apps(host, scope):
    apps = resolved(host, scope)
    assert apps
    for app in apps:
        installed = is_installed(host, app['check'])
        if app['kind'] == 'unavailable':
            assert not installed, app['app']
        else:
            assert installed, app['app']


def test_user_flatpaks_are_per_user(host):
    for app in resolved(host, 'user'):
        if app['kind'] == 'flatpak':
            f = host.file(f"{USER_HOME}/.local/share/flatpak/app/{app['flatpak']}")
            assert f.is_directory
            assert f.user == 'user'
            assert not host.file(f"/var/lib/flatpak/app/{app['flatpak']}").exists
