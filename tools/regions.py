#! /usr/bin/env python2
"""
mbed SDK
Copyright (c) 2011-2013 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

LIBRARIES BUILD
"""
from __future__ import print_function, division, absolute_import

import sys
from os.path import join, abspath, dirname
import json


# Be sure that the tools directory is in the search path
ROOT = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from tools.build_api import merge_region_list
from tools.notifier.term import TerminalNotifier
from tools.config import Region
if __name__ == '__main__':
    with open(join("region_list.json"), "r") as region_list_file:
        region_list_data = json.load(region_list_file)
    region_list = [Region(*r) for r in region_list_data]
    merge_region_list(
        region_list,
        "BUILD/mbed-cloud-client-example.hex",
        TerminalNotifier()
    )

    sys.exit(0)
