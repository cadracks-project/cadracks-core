# coding: utf-8

# Copyright 2018-2019 Guillaume Florent, Thomas Paviot, Bernard Uguen

# This file is part of cadracks-core.
#
# cadracks-core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# cadracks-core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cadracks-core.  If not, see <https://www.gnu.org/licenses/>.

r"""Utilities to group a STEP file and a part data file in a zip file"""

import logging

from os.path import basename, splitext, dirname, join
import zipfile
import json

logger = logging.getLogger(__name__)


def create_stepzip(step_file, part_data_json_file):
    r"""Procedure to create a zip file from a STEP file and an anchors file

    Parameters
    ----------
    step_file : str
        Path to the STEP file
    part_data_json_file : str
        Path to the JSON part data file

    """
    zf = zipfile.ZipFile("%s/%s.zip" % (dirname(step_file),
                                        basename(splitext(step_file)[0])),
                         "w",
                         zipfile.ZIP_DEFLATED)
    zf.write(step_file, basename(step_file))
    zf.write(part_data_json_file, basename(part_data_json_file))
    zf.close()


def extract_stepzip(stepzip):
    r"""Extract the contents of a STEP + anchors zip file

    Parameters
    ----------
    stepzip : str
        Path to the STEP + anchors zip file

    Returns
    -------
    Tuple[str, str] : path to the STEP file, path to the part data file

    """
    zip_ref = zipfile.ZipFile(stepzip)
    step_file_path, part_data_file_path = None, None

    if len(zip_ref.namelist()) != 2:
        msg = "The zip file should contain 2 files"
        raise ValueError(msg)

    for name in zip_ref.namelist():
        # bname, ext = splitext(name)
        _, ext = splitext(name)
        if ext in [".stp", ".step", ".STP", ".STEP"]:
            step_file_path = join(dirname(stepzip), name)
        elif ext in [".json", ".JSON"]:
            part_data_file_path = join(dirname(stepzip), name)
        else:
            msg = f"Unknown file type in zip with extension {ext}"
            logger. error(msg)
            raise ValueError(msg)
    zip_ref.extractall(dirname(stepzip))
    zip_ref.close()
    return step_file_path, part_data_file_path


def read_part_data(json_filename):
    r"""(New style) stepzip files contain a 'part_data.json'. This function
    read the part_data.json file to extract anchors and properties

    Parameters
    ----------
    json_filename : str
        Path to the part_data.json file

    Returns
    -------
    tuple(dict, dict)
        A tuple with the anchors dictionary and the properties dictionary
    """

    with open(json_filename) as data_file:
        json_file_content = json.load(data_file)

    anchors = json_file_content["anchors"]

    try:
        properties = json_file_content["properties"]
    except KeyError:
        properties = {}

    return anchors, properties
