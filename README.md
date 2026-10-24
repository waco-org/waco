# Waco - Workstation as Code

An Ansible collection, `waco_org.waco`, to provision developer workstations.

**Status:** work in progress, not yet released. See the
[plan](https://github.com/waco-org/waco-docs/blob/main/review-and-plan.md).

## Usage

The `workstation` role applies the other roles, selected by variables in the inventory:

```yaml
# host_vars/myhost.yml
waco_has_vscode: true
waco_has_docker: true
docker_users: [nick]
waco_packages: [vim-X11]
waco_users: [nick]
waco_user_settings:
  nick:
    has_rust: true
    python_versions: ["3.13"]
    python_tools: [{name: tox, with: [tox-uv]}]
```

    ansible-playbook -i inventory --ask-become-pass waco_org.waco.workstation

Each role documents its variables in `meta/argument_specs.yml`; `ansible-doc -t role
waco_org.waco.<role>` shows them.

| Role | Installs |
|------|----------|
| `workstation` | everything below, as selected by the `waco_*` variables |
| `base` | EPEL and CodeReady Builder on EL; apt repository prerequisites on Ubuntu |
| `packages` | distro packages |
| `users` | user accounts |
| `flatpak` | Flathub apps, system-wide or per user (Red Hat family only for now) |
| `docker` | Docker CE (via `nmusatti.docker_ce`) and per-user access through the `docker` group, which is root-equivalent |
| `dropbox` | Dropbox: the Flathub app on the Red Hat family, `nautilus-dropbox` on Ubuntu |
| `grsync` | grsync, where the distro has it (not on EL10) |
| `maven` | the distro's Apache Maven; projects needing a specific release use `mvnw` |
| `hashicorp` | Packer, Vagrant and other packages from HashiCorp's repository |
| `virtualbox` | Oracle VirtualBox from Oracle's repository |
| `vscode` | Visual Studio Code from Microsoft's repository |
| `rust` | Rust via rustup, per user |
| `python` | uv system-wide; Python versions and tools per user, with uv |

The distro Python is left to the system. Python versions for development come from uv.

## Supported platforms

Every release of Rocky Linux, Fedora and Ubuntu LTS that is in active maintenance (not just
security fixes), and, with lower priority, CentOS Stream. The current list is in
[extensions/molecule/distros](extensions/molecule/distros).

## Development

Tests use [Molecule](https://ansible.readthedocs.io/projects/molecule/) with rootless
[Podman](https://podman.io/) containers that run systemd. You need Podman and Python 3.12 or
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
(`yamllint`, `ansible-lint`).

## License

GPLv3 or later.
