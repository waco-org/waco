import json
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# The same assertions on every distro: each app is checked as the catalog
# says, and the catalog says where it is unavailable.

COMMAND_DIRS = ['/var/lib/flatpak/exports/bin', '/snap/bin']

DESKTOP_DIRS = ['/usr/share/applications',
                '/var/lib/flatpak/exports/share/applications',
                '/var/lib/snapd/desktop/applications']


def resolved(host):
    return json.loads(host.file('/var/tmp/waco-apps-system.json').content_string)


def is_installed(host, check):
    if 'command' in check:
        name = check['command']
        return host.exists(name) or any(
            host.file(f'{d}/{name}').exists for d in COMMAND_DIRS)
    if 'desktop' in check:
        return any(host.file(f"{d}/{check['desktop']}.desktop").exists
                   for d in DESKTOP_DIRS)
    raise ValueError(f'unknown check {check}')


def test_apps(host):
    apps = resolved(host)
    assert apps
    for app in apps:
        installed = is_installed(host, app['check'])
        if app['kind'] == 'unavailable':
            assert not installed, app['app']
        else:
            assert installed, app['app']
