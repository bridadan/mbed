import six
from builtins import super
from enum import Enum
from abc import ABCMeta, abstractmethod
from ..config import ConfigException

# For a summary of all the options, Wikipedia has some great tables:
# https://en.wikipedia.org/wiki/ARM_Cortex-M

ArmArchitecture = Enum("ArmArchitecture", "v6m v7a v7m v8m")
FloatingPoint = Enum("FloatingPoint", "single_precision double_precision")

_CORE_MAP = {
    "Cortex-A9": {
        "core": "cortex-a9",
        "fpu": "double_precision",
    },
    "Cortex-M0": {
        "core": "cortex-m0",
    },
    "Cortex-M0+": {
        "core": "cortex-m0plus",
    },
    "Cortex-M1": {
        "core": "cortex-m1",
    },
    "Cortex-M3": {
        "core": "cortex-m3",
    },
    "Cortex-M4": {
        "core": "cortex-m4",
    },
    "Cortex-M4F": {
        "core": "cortex-m4",
        "fpu": "single_precision",
    },
    "Cortex-M7": {
        "core": "cortex-m7",
    },
    "Cortex-M7F": {
        "core": "cortex-m7",
        "fpu": "single_precision",
    },
    "Cortex-M7FD": {
        "core": "cortex-m7",
        "fpu": "double_precision",
    },
    "Cortex-M23-NS": {
        "core": "cortex-m23",
        "tz": True,
    },
    "Cortex-M23": {
        "core": "cortex-m23",
        "tz": True,
    },
    "Cortex-M33-NS": {
        "core": "cortex-m33",
        "tz": True,
    },
    "Cortex-M33": {
        "core": "cortex-m33",
        "tz": True,
    },
    "Cortex-M33F-NS": {
        "core": "cortex-m33",
        "fpu": "single_precision",
        "tz": True,
    },
    "Cortex-M33F": {
        "core": "cortex-m33",
        "fpu": "single_precision",
        "tz": True,
    },
    "Cortex-M33FD-NS": {
        "core": "cortex-m33",
        "fpu": "double_precision",
        "tz": True,
    },
    "Cortex-M33FD": {
        "core": "cortex-m33",
        "fpu": "double_precision",
        "tz": True,
    },
}

_CORE_EXTENSIONS = {
    "coretx-m4": {
        "dsp": True,
    }
}

class Core(object):

    CORE_FPUS = {
        "cortex-m4": {
            FloatingPoint.single_precision: "fpv4-sp-d16",
        },
        "cortex-m7": {
            FloatingPoint.single_precision: "fpv5-sp-d16",
            FloatingPoint.double_precision: "fpv5-d16",
        },
        "cortex-m33": {
            FloatingPoint.single_precision: "fpv5-sp-d16",
        },
        "cortex-a9": {
            FloatingPoint.double_precision: "vfpv3"
        },
    }

    def __init__(self, core, tz=False, fp=None, dsp=None):
        self._core = core
        self._tz = tz
        fp = FloatingPoint[fp] if fp else None

        try:
            self._fp = self.CORE_FPUS[self._core][self._fp] if self._fp else None
        except KeyError:
            supported_fps = [
                fp.name for fp in self.CORE_FPUS.get(self._core, {}).keys()
            ]

            err_msg = 'Invalid floating point setting "{}" for core {}". '.format(
                self._fp, self._core
            )

            if supported_fps:
                err_msg += "This core does not support hardware floating point."
            else:
                err_msg += "Valid floating point settings are: {}".format(self._fp)

            raise ConfigException(err_msg)

        # Certain cores (Cortex-M4) always have the DSP extension present
        # Enable the extension by default if not explicitly set in the constructor
        if dsp is None:
            self._dsp = _CORE_EXTENSIONS.get(core, {}).get("dsp", False)
        else:
            self._dsp = dsp

    @property
    def core(self):
        return self._core

    @property
    def tz(self):
        return self._tz

    @property
    def fp(self):
        return self.CORE_FPUS[self._core][self._fp] if self._fp else None

    @property
    def dsp(self):
        return self._dsp

def create_cores(data):
    """data can be a string, and dict, or an array of dicts"""
    if isinstance(data, six.string_types):
        data = _CORE_MAP[data]

    if not isinstance(data, dict):
        raise TypeError("A core must either be a string or a dictionary")

    core = data["core"]
    del data["core"]
    return Core(core, **data)
