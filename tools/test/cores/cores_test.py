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
from tools.cores import Core, FloatingPointUnit, create_core
from tools.config import ConfigException

class CoreTest(unittest.TestCase):
    """
    Test cases for Core Api
    """


    def test_create_core_string(self):
        fake_core_map = {
            "fake_core": {
                "name": "core_value",
                "arg": "arg_value",
            }
        }
        with patch.dict("tools.cores._CORE_MAP", fake_core_map),\
            patch("tools.cores.Core") as patched_Core:
            _ = create_core("fake_core")
            patched_Core.assert_called_with("core_value", arg="arg_value")

    def test_create_core_dict(self):
        with patch("tools.cores.Core") as patched_core:
            _ = create_core({
                "name": "fake_core",
                "arg": "arg_value",
                "arg2": "arg2_value"
            })
            patched_core.assert_called_with(
                "fake_core", arg="arg_value", arg2="arg2_value"
            )

    def test_create_core_invalid(self):
        type_error = None
        try:
            _ = create_core(1234)
        except TypeError as e:
            type_error = e

        assert type_error

    def test_core_invalid_fpu(self):
        patched_core_fpus = {
            "fake_core": {
                FloatingPointUnit.single_precision: "fake_fpu",
            },
        }
        with patch.dict("tools.cores.Core._CORE_FPUS", patched_core_fpus):
            config_exception = None
            try:
                _ = Core("fake_core", fpu=FloatingPointUnit.double_precision)
            except ConfigException as e:
                config_exception = e

            assert config_exception

    def test_core_disabled_fpu(self):
        patched_core_fpus = {
            "fake_core": {
                FloatingPointUnit.single_precision: "fake_fpu",
            },
        }
        with patch.dict("tools.cores.Core._CORE_FPUS", patched_core_fpus):
            core = Core("fake_core", fpu=None)
            assert core.fpu is None

    def test_core_coretex_m4_default_dsp(self):
        core = Core("Cortex-M4")
        assert core.dsp is True

    def test_core_coretex_m4_overridden_dsp(self):
        """ This shouldn't ever be necessary, but you can override the Cortex-M4
        dsp extension if need be """
        core = Core("Cortex-M4", dsp=False)
        assert core.dsp is False

    def test_core_valid(self):
        patched_core_fpus = {
            "fake_core": {
                FloatingPointUnit.single_precision: "fake_fpu",
            },
        }
        with patch.dict("tools.cores.Core._CORE_FPUS", patched_core_fpus):
            config_exception = None
            core = Core(
                "fake_core",
                tz=True,
                fpu=FloatingPointUnit.single_precision,
                dsp=True
            )

            assert core.name == "fake_core"
            assert core.fpu == "fake_fpu"
            assert core.tz is True
            assert core.dsp is True


if __name__ == '__main__':
    unittest.main()
