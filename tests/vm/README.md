# VM tests

Waco's VM tier: full runs in VirtualBox VMs, for what the Molecule containers
can't show. Local only: GitHub's runners don't offer VirtualBox in a usable form.

The containers can't show:

- kernel modules really built and loaded (VirtualBox's `vboxdrv`);
- SELinux and AppArmor enforcing;
- firewalld zones (mDNS for printer discovery);
- services really running: CUPS, the Docker daemon, a persistent journal across a reboot;
- `waco-bootstrap` and `waco-provision` on a real install, with a real admin account;
- the desktop: Flatpaks and snaps starting, Eclipse's update check.

## Running

```sh
tests/vm/run rocky10          # up, provision, check, screenshot, destroy
tests/vm/run -k fedora45      # keep the VM: vagrant ssh fedora45 (from tests/vm)
```

The machines are the entries of [boxes.yml](boxes.yml): `rocky10`, `fedora44`,
`fedora45` and `ubuntu2604`. By default a run covers one per family: Rocky 10, the
latest Fedora, the latest Ubuntu LTS.

A run tests the **committed** state of this checkout and of the `waco-bootstrap`
checkout next to it (or `$WACO_BOOTSTRAP`). Each VM gets:

1. `disk`: the root file system grown to the 40 GB disk;
2. `desktop`: the distro's GNOME workstation (`WACO_VM_DESKTOP=no` skips it);
3. `upload`: bundles of both repositories and the test settings;
4. `bootstrap`: the settings clone in `~vagrant/.waco` with the test settings
   ([overlay/](overlay/)) committed, then `waco-bootstrap`;
5. `provision`: `waco-provision` with the collection under test;
6. `check`: [guest/check](guest/check), which reports every check and fails if
   any did.

The log and a screenshot land in `tests/vm/out/`.

`vagrant` is the VM's admin, with uid 1000, so the docker role's uid-1000 account is
skipped with a warning, as on a machine whose first user took 1000.

## Host setup

- Vagrant and VirtualBox (Waco's `vagrant` and `virtualbox` apps).
- `xorriso`, for the cloud-init seed of boxes made from cloud images (Vagrant's
  `cloud_init`, enabled by `run` through `VAGRANT_EXPERIMENTAL`).
- VirtualBox's machine folder somewhere with room: a VM with a desktop takes
  15–20 GB. On imladris: `/vm/main`.

## Boxes

Only official images, checked against the distro's signed checksums:

| Machine | Image | Checksums signed by |
|---|---|---|
| `rocky10` | Rocky's Vagrant box | `CHECKSUM.asc`, Rocky Linux 10 release key `FC22 6859 C086 0BF0 DDB9 5B08 5B10 6C73 6FED FC85` |
| `fedora44`, `fedora45` | Fedora Cloud's Vagrant box | the `CHECKSUM` file is signed inline with the release's key, from <https://fedoraproject.org/fedora.gpg> |
| `ubuntu2604` | Ubuntu's cloud image OVA, made into a box by `add-box` | `SHA256SUMS.gpg`, UEC Image Automatic Signing Key `D2EB 4462 6FDD C30B 513D 5BB7 1A5D 6C4C 7DB8 7C81` |

Canonical stopped publishing Vagrant boxes after 22.04. Third-party boxes (Bento)
were considered and rejected: no published checksums.

To update an entry: download the new checksum file and its signature, check the
signature (`gpg --verify`), copy the image's SHA-256 into `boxes.yml` with the new
URL and box name (the date or build in the name makes Vagrant fetch it), and remove
the old box with `vagrant box remove`.
