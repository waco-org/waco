# Changelog

## Unreleased

- Collection created from the `waco-master` and `waco-python` roles.
- Molecule test setup with Podman, without tox.
- `master` split into per-tool roles applied by the new `workstation` role, plus a
  `workstation` playbook. Variables are validated with `argument_specs`.
- Breaking changes:
  - Python: uv instead of source builds and shared virtualenvs in `/opt`; no `python` user.
    Per-user Python versions and tools are set in `waco_user_settings`.
  - Maven comes from the distro instead of an upstream archive in `/opt`.
  - Docker: no `docker` user; `docker_users` are added to the `docker` group.
  - The component variables are renamed after their roles (`wavb_release` is now
    `virtualbox_release`, and so on); `waco_install_dir`, `waco_software_dir` and the unused
    `waco_docker_uid`, `wapa_disable_repo`, `wavb_disable_repo` and `wado_compose_version` are
    gone.
- Fixes: Dropbox no longer depends on `waco_flatpak_apps`; grsync is skipped with a warning
  where the distro has none (EL10); vendor repositories use `yum_repository` and
  `deb822_repository` instead of `yum-config-manager` and `apt_key` (Ubuntu 26.04); Rust uses
  the user's real home and a private temporary file; CRB is really enabled on EL; no more EL8
  and Python 2 code.
