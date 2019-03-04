import six
import copy
from builtins import super
from enum import Enum
from abc import ABCMeta, abstractmethod
from ..config import ConfigException

# For a summary of all the options, Wikipedia has some great tables:
# https://en.wikipedia.org/wiki/ARM_Cortex-M

ArmArchitecture = Enum("ArmArchitecture", "v6m v7a v7m v8m")
FloatingPointUnit = Enum("FloatingPointUnit", "single_precision double_precision")

# TODO move to lower case
_CORE_MAP = {
    "Cortex-A9": {
        "name": "Cortex-A9",
        "fpu": "double_precision",
    },
    "Cortex-M0": {
        "name": "Cortex-M0",
    },
    "Cortex-M0+": {
        "name": "Cortex-M0Plus",
    },
    "Cortex-M1": {
        "name": "Cortex-M1",
    },
    "Cortex-M3": {
        "name": "Cortex-M3",
    },
    "Cortex-M4": {
        "name": "Cortex-M4",
    },
    "Cortex-M4F": {
        "name": "Cortex-M4",
        "fpu": "single_precision",
    },
    "Cortex-M7": {
        "name": "Cortex-M7",
    },
    "Cortex-M7F": {
        "name": "Cortex-M7",
        "fpu": "single_precision",
    },
    "Cortex-M7FD": {
        "name": "Cortex-M7",
        "fpu": "double_precision",
    },
    "Cortex-M23-NS": {
        "name": "Cortex-M23",
        "tz": True,
    },
    "Cortex-M23": {
        "name": "Cortex-M23",
        "tz": True,
    },
    "Cortex-M33-NS": {
        "name": "Cortex-M33",
        "tz": True,
    },
    "Cortex-M33": {
        "name": "Cortex-M33",
        "tz": True,
    },
    "Cortex-M33F-NS": {
        "name": "Cortex-M33",
        "fpu": "single_precision",
        "tz": True,
    },
    "Cortex-M33F": {
        "name": "Cortex-M33",
        "fpu": "single_precision",
        "tz": True,
    },
    "Cortex-M33FD-NS": {
        "name": "Cortex-M33",
        "fpu": "double_precision",
        "tz": True,
    },
    "Cortex-M33FD": {
        "name": "Cortex-M33",
        "fpu": "double_precision",
        "tz": True,
    },
}


class Core(object):

    # TODO move keys to lowercase
    _CORE_FPUS = {
        "Cortex-M4": {
            FloatingPointUnit.single_precision: "fpv4-sp-d16",
        },
        "Cortex-M7": {
            FloatingPointUnit.single_precision: "fpv5-sp-d16",
            FloatingPointUnit.double_precision: "fpv5-d16",
        },
        "Cortex-M33": {
            FloatingPointUnit.single_precision: "fpv5-sp-d16",
        },
        "Cortex-A9": {
            FloatingPointUnit.double_precision: "vfpv3"
        },
    }

    def __init__(self, name, tz=False, fpu=None, dsp=None):
        self._name = name
        self._tz = tz
        self._fpu = fpu

        if not self.is_valid_fpu(self._name, self._fpu):
            supported_fpus = [
                f.name for f in self._CORE_FPUS.get(self._name, {}).keys()
            ]

            err_msg = 'Invalid fpu value "{}" for core {}". '.format(
                self._fpu, self._name
            )

            if supported_fpus:
                err_msg += "This core does not support hardware floating point."
            else:
                err_msg += "Valid fpu values are: {}".format(self._fpu)

            raise ConfigException(err_msg)

        # The Cortex-M4 always has the DSP extension present. Enable the extension
        # by default if not explicitly set to False.
        if dsp is None and self._name == "Cortex-M4":
            self._dsp = True
        else:
            self._dsp = dsp

    @property
    def name(self):
        return self._name

    @property
    def tz(self):
        return self._tz

    @property
    def fpu(self):
        return self._CORE_FPUS[self._name][self._fpu] if self._fpu else None

    @property
    def dsp(self):
        return self._dsp

    @classmethod
    def is_valid_fpu(self, core_name, fpu):
        return fpu is None or fpu in self._CORE_FPUS.get(core_name, {})

def create_core(data):
    """data can be a string, and dict, or an array of dicts"""
    if isinstance(data, six.string_types):
        data = _CORE_MAP[data]
    if not isinstance(data, dict):
        raise TypeError(
            "The provided type was {}. A core must either be a string or a "
            "dictionary.".format(type(data))
        )

    name = data["name"]
    core_data = { k: v for k, v in data.items() if k != "name" }

    if "fpu" in core_data:
        core_data["fpu"] = FloatingPointUnit[core_data["fpu"]] if core_data["fpu"] else None

    return Core(name, **core_data)
