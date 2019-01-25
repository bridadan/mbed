"""
mbed SDK
Copyright (c) 2019 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
from mock import patch, MagicMock
from tools.cores import Core, create_cores

class CoreTest(unittest.TestCase):
    """
    Test cases for Build Api
    """


    def test_create_cores_string(self, *_):
        fake_core_map = {
            "fake_core": {
                "core": "core_value",
                "arg": "arg_value",
            }
        }
        with patch.dict("tools.cores._CORE_MAP", fake_core_map),\
            patch("tools.cores.Core") as patched_Core:
            _ = create_cores("fake_core")
            patched_Core.assert_called_with("core_value", arg="arg_value")


if __name__ == '__main__':
    unittest.main()
