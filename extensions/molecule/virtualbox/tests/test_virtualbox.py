import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_virtualbox(host):
    assert host.run('vboxmanage --version').rc == 0


def test_module_build_tools(host):
    # What vboxconfig and vboxdrv.service need to build the kernel modules;
    # the build itself only happens outside containers (tests/vm).
    for tool in ('gcc', 'make', 'perl'):
        assert host.exists(tool)
    if host.system_info.distribution == 'ubuntu':
        headers = [n for n in host.file('/usr/src').listdir() if n.startswith('linux-headers-')]
    else:
        headers = host.file('/usr/src/kernels').listdir()
    assert headers
