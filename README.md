# 📚 docs.octoprint.org

You are looking at the files used to build [OctoPrint's](https://octoprint.org) documentation
as published on [docs.octoprint.org](https://docs.octoprint.org).

It is implemented through the github workflow under `.github/workflows/docs.yaml` and relies
on a custom sphinx wrapper located in `util/versionselector` as well as a little helper
located in `util/versions_from_matrix.py`.

**Builds are triggered** via a webhook from [OctoPrint/OctoPrint](https://github.com/OctoPrint/OctoPrint)
on pushes and new tagged releases, and on push to `master` on this repository.

Webhook triggers cause only a single doc version to be rebuilt (if any). Pushes however trigger 
a full rebuild of all registered doc versions.

**To register a new version to be built and served**, edit the build matrix configured
in `.github/workflows/docs.yaml`. Do not use anything but `include` statements for that or
the version extraction during build will no longer work.
