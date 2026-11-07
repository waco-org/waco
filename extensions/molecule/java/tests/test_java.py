import json
import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# The same assertions on every distro: each JDK reports its version and
# comes from its source, and the newest one is the default.

DEFAULT = 25


def jdks(host):
    return json.loads(host.file('/var/tmp/waco-java.json').content_string)


def version(output):
    """The major version in the output of java -version or javac -version."""
    match = re.search(r'(?:version "|javac )(?:1\.)?(\d+)', output)
    assert match, output
    return int(match[1])


def test_jdks(host):
    found = jdks(host)
    assert sorted(j['version'] for j in found) == [11, 21, 25]
    for jdk in found:
        out = host.run(f"{jdk['home']}/bin/java -version").stderr
        assert version(out) == jdk['version'], out
        assert ('Temurin' in out) == (jdk['source'] == 'temurin'), out
        assert host.file(f"{jdk['home']}/bin/javac").exists


def test_default(host):
    assert version(host.run('java -version').stderr) == DEFAULT
    assert version(host.check_output('javac -version')) == DEFAULT


def test_java_home(host):
    home = host.check_output("bash -lc 'echo $JAVA_HOME'")
    assert home
    assert version(host.check_output(f'{home}/bin/javac -version')) == DEFAULT
