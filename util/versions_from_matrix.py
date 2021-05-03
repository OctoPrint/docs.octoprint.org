# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2020 The OctoPrint Project - Released under terms of the AGPLv3 License"

import json
import sys

import yaml

if __name__ == "__main__":
    workflow_path = sys.argv[1]
    versions_path = sys.argv[2]

    with open(workflow_path, mode="r", encoding="utf8") as f:
        data = yaml.safe_load(f)

    matrix = data["jobs"]["build"]["strategy"]["matrix"]["include"]
    print(repr(matrix))

    versions = dict()
    for version in matrix:
        name = version["version"]
        source = version["source"]
        print("Adding {}/{} to versions.json".format(name, source))

        versions[name] = dict(
            name=name,
            url="https://docs.octoprint.org/en/{}".format(name),
            is_released=source == "tags",
            source=source,
        )

    with open(versions_path, mode="w", encoding="utf8") as f:
        json.dump(versions, f)

    print("versions.json dumped at {}".format(versions_path))
