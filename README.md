# Waco - Workstation as Code

An Ansible collection, `waco_org.waco`, to provision developer workstations.

> **Work in progress: not ready for use.** The collection is being restructured and is not yet
> released; roles, variables and behaviour may change without notice.

## Usage

The `workstation` role applies the other roles, selected by variables in the inventory:

```yaml
# host_vars/myhost.yml
waco_apps: [vscode, grsync, eclipse, virtualbox]
eclipse_plugins:
  - {repository: "https://www.pydev.org/updates", iu: org.python.pydev.feature.feature.group}
waco_has_docker: true
docker_users: [nick]
waco_has_java: true
java_versions: [25, 21, 11]
waco_packages: [vim-X11]
waco_printing_queues:
  - {name: office, uri: "ipp://10.0.0.24/ipp/print", description: Office printer, default: true}
waco_sudoers:
  - {name: nick-true, content: "nick ALL=(root) NOPASSWD: /usr/bin/true\n"}
waco_users:
  - {name: nick, uid: 1001, admin: true, groups: [vboxusers]}
```

    ansible-playbook -i inventory --ask-become-pass waco_org.waco.workstation

Apps are named in the app catalog, `roles/apps/vars/catalog.yml`, which says where each one
comes from on each platform: a distro package, a flatpak, a snap or a per-tool role.
`waco_packages` and `waco_flatpak_apps` remain for anything not in the catalog.
[docs/apps.md](docs/apps.md) shows the result for each distribution.

Waco installs system-wide, for every user of the machine. Apart from creating the accounts,
it leaves home directories alone: per-user tools such as rustup, uv-managed Pythons or per-user
flatpaks are for each user to install, or for a home-directory tool.

Each role documents its variables in `meta/argument_specs.yml`; `ansible-doc -t role
waco_org.waco.<role>` shows them.

| Role | Installs |
|------|----------|
| `workstation` | everything below, as selected by the `waco_*` variables |
| `base` | EPEL and CodeReady Builder on EL; apt repository prerequisites on Ubuntu |
| `system` | mDNS through firewalld, so that printers and scanners are discovered; a persistent journal; sudoers drop-ins checked with `visudo`. Fedora and Ubuntu already have the first two |
| `printing` | permanent CUPS print queues, driverless or with their own PPD; discovered printers get temporary queues without it |
| `packages` | distro packages |
| `users` | user accounts |
| `apps` | the apps in the catalog, each from its source for the platform |
| `flatpak` | Flathub apps, system-wide |
| `snap` | snaps (Ubuntu only) |
| `docker` | Docker CE (via `nmusatti.docker_ce`) and per-user access through the `docker` group, which is root-equivalent |
| `eclipse` | the Eclipse IDE for Java Developers from eclipse.org: by default the newest December release, plus its predecessor as a fallback; plugins with the p2 director |
| `java` | JDKs: the distro's OpenJDK where it is packaged and maintained, Eclipse Temurin otherwise; the default JDK and `JAVA_HOME` |
| `maven` | the distro's Apache Maven; projects needing a specific release use `mvnw` |
| `hashicorp` | Packer, Vagrant and other packages from HashiCorp's repository |
| `virtualbox` | Oracle VirtualBox from Oracle's repository |
| `vscode` | Visual Studio Code from Microsoft's repository |
| `python` | uv system-wide |

The distro Python is left to the system. Python versions for development come from uv, which
each user runs in their own home.

## Supported platforms

Every release of Rocky Linux, Fedora and Ubuntu LTS that is in active maintenance (not just
security fixes), and, with lower priority, CentOS Stream. The current list is in
[extensions/molecule/distros](extensions/molecule/distros).

## Development

Tests use [Molecule](https://ansible.readthedocs.io/projects/molecule/) with rootless
[Podman](https://podman.io/) containers that run systemd. You need Podman and Python 3.13 or
later.

    uv venv --python 3.13 .venv
    source .venv/bin/activate
    uv pip install -r requirements-dev.txt

Run every scenario on every distribution, two at a time:

    scripts/molecule-matrix

or select some of them:

    scripts/molecule-matrix -d rockylinux10 -d ubuntu2404 -s workstation-default -j 4

Logs are written to `.cache/molecule-logs`. The scenarios are in `extensions/molecule`, and their
shared settings are in `.config/molecule/config.yml`. Test images are built by Molecule from
`extensions/molecule/Dockerfile.j2`; the target distribution is chosen with the
`MOLECULE_DISTRO` environment variable. Each role has a scenario of its own, and
`workstation-complete` applies them all together.

GitHub Actions runs the same script for each distribution and scenario, plus a lint job
(`yamllint`, `ansible-lint`, `scripts/apps-table --check`).

After changing the catalog, run the `apps` scenario and then `scripts/apps-table`, which
regenerates `docs/apps.md` from the catalog and marks each source that the logs in
`.cache/molecule-logs` show as tested.

## License

GPLv3 or later.
