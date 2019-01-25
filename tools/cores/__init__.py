import six
from builtins import super
from enum import Enum
from abc import ABCMeta, abstractmethod

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

    def __init__(self, core, fp=None, dsp=None, tz=False):
        self.core = core
        self.tz = tz
        self._fp = None if fp is None else FloatingPoint[fp]
        
        # Certain cores (Cortex-M4) always have the DSP extension present
        # Enable the extension by default if not explicitly set in the constructor
        if dsp is None:
            self.dsp = _CORE_EXTENSIONS.get(core, {}).get("dsp", False)
        else:
            self.dsp = dsp

    @property
    def fp(self):
        return None if self._fp is None else self.CORE_FPUS[self.core][self._fp]

def create_cores(data):
    """data can be a string, and dict, or an array of dicts"""
    if isinstance(data, six.string_types):
        data = _CORE_MAP[data]

    if not isinstance(data, dict):
        raise TypeError("A core must either be a string or a dictionary")

    core = data["core"]
    del data["core"]
    return Core(core, **data)
