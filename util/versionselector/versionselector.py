# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import collections
import json
import logging

DATE_FMT = "%Y-%m-%d %H:%M:%S %z"

logger = logging.getLogger(__name__)

Version = collections.namedtuple("Version", ["name", "url", "is_released", "source"])


class VersionInfo:
    def __init__(self, app, context, metadata, current_version_name):
        self.app = app
        self.context = context
        self.metadata = metadata
        self.current_version_name = current_version_name

    def _dict_to_versionobj(self, v):
        return Version(
            name=v["name"], url=v["url"], is_released=v["is_released"], source=v["source"]
        )

    @property
    def tags(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if v["source"] == "tags"
        ]

    @property
    def branches(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if v["source"] != "tags"
        ]

    @property
    def releases(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if v["is_released"]
        ]

    @property
    def in_development(self):
        return [
            self._dict_to_versionobj(v)
            for v in self.metadata.values()
            if not v["is_released"]
        ]

    def __iter__(self):
        for item in self.tags:
            yield item
        for item in self.branches:
            yield item

    def __getitem__(self, name):
        v = self.metadata.get(name)
        if v:
            return self._dict_to_versionobj(v)

    def vhasdoc(self, other_version_name):
        if self.current_version_name == other_version_name:
            return True

        other_version = self.metadata[other_version_name]
        return self.context["pagename"] in other_version["docnames"]


def html_page_context(app, pagename, templatename, context, doctree):
    if not app.config.versionselector_current_version:
        return

    if not app.config.versionselector_metadata_path:
        return

    metadata = app.config.versionselector_metadata
    if not metadata:
        with open(app.config.versionselector_metadata_path, mode="r") as f:
            metadata = json.load(f)
        app.config.versionselector_metadata = metadata
        print("versionselector metadata: {!r}".format(metadata))

    versioninfo = VersionInfo(
        app, context, metadata, app.config.versionselector_current_version
    )

    context["versions"] = versioninfo
    context["current_version"] = versioninfo[app.config.versionselector_current_version]
    context["latest_version"] = versioninfo[app.config.versionselector_latest_version]


def setup(app):
    app.add_config_value("versionselector_metadata", {}, "html")
    app.add_config_value("versionselector_metadata_path", "", "html")
    app.add_config_value("versionselector_current_version", "", "html")
    app.add_config_value("versionselector_latest_version", "master", "html")

    app.connect("html-page-context", html_page_context)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


if __name__ == "__main__":
    import os
    import sys

    argv_prefix = []
    try:
        from sphinx.cmd import build

        sphinx_build = build.main
    except ImportError:
        from sphinx import build_main as sphinx_build

        argv_prefix = ["sphinx-build"]

    from sphinx import config as sphinx_config

    if not hasattr(sphinx_config.Config, "read"):
        from sphinx.util.tags import Tags

        sphinx_config.Config.read = staticmethod(
            lambda path: sphinx_config.Config(
                path, os.path.join(path, "conf.py"), {}, Tags()
            )
        )

    if len(sys.argv) < 5:
        print(
            "versionselector.py DOCSFOLDER CURRENT LATEST METADATA [ ADDITIONAL ]",
            file=sys.stderr,
        )
        sys.exit(-1)

    docsfolder = sys.argv[1]
    current = sys.argv[2]
    latest = sys.argv[3]
    metadata = sys.argv[4]
    add_argv = sys.argv[5:] if len(sys.argv) > 5 else []

    basefolder = os.path.dirname(os.path.abspath(__file__))
    docsfolder = os.path.abspath(os.path.join(basefolder, docsfolder))

    template_path = os.path.join(basefolder, "_templates")
    css_addition = os.path.join(basefolder, "_static", "versioninfo.css")

    sys.path.insert(0, basefolder)

    config = sphinx_config.Config.read(docsfolder)
    extensions = ",".join(
        config.extensions
        + [
            "versionselector",
        ]
    )
    templates = ",".join(
        config.templates_path
        + [
            os.path.relpath(template_path, docsfolder),
        ]
    )

    argv = (
        [
            "-D",
            "versionselector_metadata_path={metadata}",
            "-D",
            "versionselector_current_version={current}",
            "-D",
            "versionselector_latest_version={latest}",
            "-D",
            "version={current}",
            "-D",
            "release={current}",
            "-D",
            "templates_path={templates}",
            "-D",
            "extensions={extensions}",
            "{docsfolder}",
        ]
        + add_argv
        + [
            "_build/html/{current}",
        ]
    )
    if argv_prefix:
        argv = argv_prefix + argv

    mapping = locals()
    argv = list(map(lambda x: x.format(**mapping), argv))

    cwd = os.getcwd()
    os.chdir(docsfolder)

    print("Running sphinx-build {}".format(" ".join(argv)))

    try:
        status = sphinx_build(argv)
        if status not in (0, None):
            print("sphinx build failed", file=sys.stderr)
            sys.exit(-2)
    finally:
        os.chdir(cwd)
