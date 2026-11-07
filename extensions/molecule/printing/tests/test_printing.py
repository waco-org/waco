import json
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def lpstat(host, *args):
    return host.run('lpstat ' + ' '.join(args))


def test_queue_with_ppd(host):
    out = lpstat(host, '-l', '-p', 'waco-ppd').stdout
    assert 'Description: Waco test printer' in out
    assert 'Location: Nowhere' in out
    assert 'ipp://192.0.2.1/ipp/print' in lpstat(host, '-v', 'waco-ppd').stdout
    ppd = host.file('/etc/cups/ppd/waco-ppd.ppd').content_string
    assert '*cupsFilter2: "image/pwg-raster image/pwg-raster 100 -"' in ppd


def test_not_shared(host):
    out = host.run('lpoptions -p waco-ppd').stdout
    assert 'printer-is-shared=false' in out


def test_default(host):
    assert lpstat(host, '-d').stdout.strip().endswith(': waco-ppd')


def test_settings_recorded(host):
    settings = json.loads(host.file('/etc/waco/cups/waco-ppd.json').content_string)
    assert settings['uri'] == 'ipp://192.0.2.1/ipp/print'
    assert settings['ppd_sha256']


def test_printer_off_skipped(host):
    assert lpstat(host, '-v', 'waco-off').rc != 0
    assert not host.file('/etc/waco/cups/waco-off.json').exists


def test_other_queues(host):
    assert lpstat(host, '-v', 'handmade').rc == 0
    assert lpstat(host, '-v', 'old').rc != 0
