# Changelog

## Unreleased

- App catalog: `waco_apps` names apps, and the new `apps` role installs each one from its
  source for the platform (distro package, flatpak, snap or per-tool role), as recorded in
  `roles/apps/vars/catalog.yml`. An app without a source fails the run unless
  `waco_apps_allow_missing` is set. Users can have `apps` too.
- `docs/apps.md`: the app × distribution table, generated from the catalog and the test logs
  by `scripts/apps-table`.
- `flatpak` works on Ubuntu; new `snap` role (Ubuntu only).
- New `java` role, selected by `waco_has_java`: the JDKs in `java_versions`, from the distro's
  OpenJDK where it is packaged and maintained, from Eclipse Temurin (Adoptium's repository)
  otherwise. `java_default` is set with `update-alternatives` in manual mode, and
  `/etc/profile.d/waco-java.sh` sets `JAVA_HOME` from it.
- `waco_users` entries can be dicts with `uid`, `gid`, `groups`, `admin`, `shell`, `comment` and
  `create_home`, besides plain names. The primary group is named after the user, with gid `gid`
  or `uid`; `admin` means `wheel` or `sudo`; new users get bash on every distro. Supplementary
  groups are added at the end of the run, so groups created by packages (`vboxusers`, `docker`)
  can be used. Waco never renumbers: an existing user with another uid, or a uid that belongs
  to someone else, fails the run.
- The `docker` role creates a `docker` account with uid 1000 (`docker_account`,
  `docker_account_uid`), which many images run as, so that files containers write to bind
  mounts have an owner name on the host. It has primary group `docker`, no login and no home,
  and is skipped with a warning if uid 1000 belongs to someone else.
- New `eclipse` role, app `eclipse` in the catalog: the Eclipse IDE for Java Developers from
  eclipse.org's archive, checked against its published SHA-512, in `/opt/eclipse-<release>`
  with a launcher. `eclipse_release` defaults to `latest`, the newest December release, so the
  install changes once a year; the previous release stays as a fallback unless
  `eclipse_keep_previous` is false. `eclipse_plugins` are installed with the p2 director.
  The update check is off.
- New `system` role, always applied by `workstation`: mDNS through firewalld's default zone
  (`waco_mdns_firewall`), so that printers and scanners are discovered on the Red Hat family; a
  persistent journal (`waco_journal_persistent`, `waco_journal_max_use`), as Fedora and Ubuntu
  already have; sudoers drop-ins (`waco_sudoers`), installed as `/etc/sudoers.d/waco-<name>`
  only if `visudo` accepts them. The first two are on by default.
- New `printing` role, applied when `waco_printing_queues` or `waco_printing_queues_absent` is
  set: permanent CUPS queues, with `lpadmin -m everywhere` or a PPD of their own. A printer
  that doesn't answer is skipped with a warning, and the next run creates its queue.
- Tests use ansible-core 2.22, the first release that runs modules on Python 3.15 (Fedora 45).
  It needs Python 3.13 or later on the controller.
- Breaking: `waco_has_dropbox`, `waco_has_grsync`, `waco_has_packer`, `waco_has_vagrant`,
  `waco_has_virtualbox` and `waco_has_vscode` are replaced by `waco_apps`, and the `dropbox`
  and `grsync` roles by catalog entries.
- Collection created from the `waco-master` and `waco-python` roles.
- Molecule test setup with Podman, without tox.
- `master` split into per-tool roles applied by the new `workstation` role, plus a
  `workstation` playbook. Variables are validated with `argument_specs`.
- Breaking changes:
  - Python: uv instead of source builds and shared virtualenvs in `/opt`; no `python` user.
    Per-user Python versions and tools are set in `waco_user_settings`.
  - Maven comes from the distro instead of an upstream archive in `/opt`.
  - Docker: `docker_users` are added to the `docker` group. The old `docker` user, which
    fell back to a random uid when 1000 was taken, is replaced by `docker_account` (see above).
  - The component variables are renamed after their roles (`wavb_release` is now
    `virtualbox_release`, and so on); `waco_install_dir`, `waco_software_dir` and the unused
    `waco_docker_uid`, `wapa_disable_repo`, `wavb_disable_repo` and `wado_compose_version` are
    gone.
- Fixes: Dropbox no longer depends on `waco_flatpak_apps`; grsync is skipped with a warning
  where the distro has none (EL10); vendor repositories use `yum_repository` and
  `deb822_repository` instead of `yum-config-manager` and `apt_key` (Ubuntu 26.04); Rust uses
  the user's real home and a private temporary file; CRB is really enabled on EL; no more EL8
  and Python 2 code.
