# Waco - Workstation as Code

An Ansible collection, `waco_org.waco`, to provision developer workstations.

**Status:** work in progress. The roles in this repository are being migrated from the
`waco-master` and `waco-python` repositories of the [waco-org](https://github.com/waco-org)
organisation and will be restructured. See the
[plan](https://github.com/waco-org/waco-docs/blob/main/review-and-plan.md).

## Supported platforms

Every release of Rocky Linux, Fedora and Ubuntu LTS that is in active maintenance (not just
security fixes), and, with lower priority, CentOS Stream. The current list is in
[extensions/molecule/distros](extensions/molecule/distros).

## Development

Tests use [Molecule](https://ansible.readthedocs.io/projects/molecule/) with rootless
[Podman](https://podman.io/) containers that run systemd. You need Podman and Python 3.12 or
later.

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt

Run every scenario on every distribution, two at a time:

    scripts/molecule-matrix

or select some of them:

    scripts/molecule-matrix -d rockylinux10 -d ubuntu2404 -s master-default -j 4

Logs are written to `.cache/molecule-logs`. The scenarios are in `extensions/molecule`, and their
shared settings are in `.config/molecule/config.yml`. Test images are built by Molecule from
`extensions/molecule/Dockerfile.j2`; the target distribution is chosen with the
`MOLECULE_DISTRO` environment variable.

GitHub Actions runs the same script for each distribution and scenario, plus a lint job
(`yamllint`, `ansible-lint`).

## License

GPLv3 or later.
