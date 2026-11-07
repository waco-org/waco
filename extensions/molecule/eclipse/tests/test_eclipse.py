import json
import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def waco_installs(host):
    out = host.check_output('ls -d /opt/eclipse-*/.waco-eclipse 2>/dev/null || true')
    return sorted(os.path.dirname(p) for p in out.split())


def release(host):
    installs = waco_installs(host)
    assert len(installs) == 1, installs
    return installs[0].removeprefix('/opt/eclipse-')


def test_latest_december_release(host):
    assert re.fullmatch(r'\d{4}-12', release(host))


def test_install(host):
    home = f'/opt/eclipse-{release(host)}'
    for path in (home, f'{home}/eclipse', f'{home}/plugins'):
        f = host.file(path)
        assert f.exists
        assert f.user == 'root'
    # The bundled JRE
    assert host.check_output(f'ls -d {home}/plugins/org.eclipse.justj.openjdk.*')
    link = host.file('/usr/local/bin/eclipse')
    assert link.is_symlink
    assert link.linked_to == f'{home}/eclipse'


def test_launcher(host):
    r = release(host)
    f = host.file(f'/usr/share/applications/waco-eclipse-{r}.desktop')
    assert f.contains(f'^Name=Eclipse {r}$')
    assert f.contains(f'^Exec=/opt/eclipse-{r}/eclipse$')


def test_update_check_off(host):
    ini = host.check_output(
        f'ls /opt/eclipse-{release(host)}/plugins/org.eclipse.epp.package.java_*/plugin_customization.ini')
    out = host.check_output(f'grep "^org.eclipse.equinox.p2.ui.sdk.scheduler/enabled=" {ini}')
    assert out == 'org.eclipse.equinox.p2.ui.sdk.scheduler/enabled=false'


def test_plugin(host):
    with host.sudo():
        out = host.check_output(
            f'HOME=$(mktemp -d) /opt/eclipse-{release(host)}/eclipse -nosplash '
            '-application org.eclipse.equinox.p2.director -listInstalledRoots')
    assert 'de.jcup.basheditor.feature.group/' in out


def test_previous_releases(host):
    first = json.loads(host.file('/var/tmp/waco-eclipse-first.json').content_string)
    assert first == {'2020-12': False, '2021-12': True}
    for r in ('2020-12', '2021-12'):
        assert not host.file(f'/opt/eclipse-{r}').exists
        assert not host.file(f'/usr/share/applications/waco-eclipse-{r}.desktop').exists


def test_other_installs_untouched(host):
    assert host.file('/opt/eclipse-4.38').is_directory
