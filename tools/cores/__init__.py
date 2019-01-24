from builtins import super
from enum import Enum
from future.utils import with_metaclass
from abc import ABCMeta, abstractmethod

# For a summary of all the options, Wikipedia has some great tables:
# https://en.wikipedia.org/wiki/ARM_Cortex-M

ArmArchitecture = Enum("ArmArchitecture", "v6m v7a v7m v8m")
FloatingPoint = Enum("FloatingPoint", "none single_precision double_precision")

class Cortex(with_metaclass(ABCMeta, object)):
    @property
    @abstractmethod
    def arch(self):
        raise NotImplementedError

class CortexM(Cortex):
    @property
    @abstractmethod
    def dsp(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def fpu(self):
        raise NotImplementedError

class CortexMV6(CortexM):
    @property
    def arch(self):
        return ArmArchitecture.v6m

    @property
    def dsp(self):
        return False

    @property
    def fpu(self):
        return FloatingPoint.none

class CortexMV7(CortexM):
    def __init__(self, dsp, fpu):
        self._dsp = dsp
        self._fpu = fpu

    @property
    def arch(self):
        return ArmArchitecture.v7m

    @property
    def dsp(self):
        return self._dsp

    @property
    def fpu(self):
        return self._fpu

class CortexMV8(CortexM):
    def __init__(self, dsp, fpu, tz):
        self._dsp = dsp
        self._fpu = fpu
        self._tz = tz

    @property
    def arch(self):
        return ArmArchitecture.v7m

    @property
    def dsp(self):
        return self._dsp

    @property
    def fpu(self):
        return self._fpu

    @property
    def tz(self):
        return self._tz

class CortexM0(CortexMV6):
    pass

class CortexM0p(CortexMV6):
    pass

class CortexM1(CortexMV6):
    pass

class CortexM3(CortexMV7):
    def __init__(self):
        super().__init__(False, False)

class CortexM4(CortexMV7):
    def __init__(self, fpu=FloatingPoint.none):
        super().__init__(True, fpu)

class CortexM7(CortexMV7):
    def __init__(self, fpu=FloatingPoint.none):
        super().__init__(True, fpu)

class CortexM23(CortexMV8):
    def __init__(self, fpu=FloatingPoint.none, tz=False):
        super().__init__(False, fpu, tz)

class CortexM33(CortexMV8):
    def __init__(self, dsp=False, fpu=FloatingPoint.none, tz=False):
        super().__init__(dsp, fpu, tz)

class CortexA(Cortex):
    @property
    @abstractmethod
    def fpu(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def tz(self):
        raise NotImplementedError

class CortexAV7(CortexA):
    def __init__(self, fpu, tz):
        self._fpu = fpu
        self._tz = tz

    @property
    def arch(self):
        return ArmArchitecture.v7a

    @property
    def fpu(self):
        return self._fpu

    @property
    def tz(self):
        return self._tz


class CortexA9(CortexAV7):
    def __init__(self, fpu=FloatingPoint.none, tz=False):
        super().__init__(dsp, fpu, tz)

LEGACY_CORE_MAPPING = {
    "Cortex-M0": CortexM0(),
    "Cortex-M0+": CortexM0p(),
    "Cortex-M1": CortexM1(),
    "Cortex-M3": CortexM3(),
    "Cortex-M4": CortexM4(),
    "Cortex-M4F": CortexM4(fpu=FloatingPoint.single_precision),
    "Cortex-M7": CortexM7(),
    "Cortex-M7F": CortexM7(fpu=FloatingPoint.single_precision),
    "Cortex-M7FD": CortexM7(fpu=FloatingPoint.double_precision),
    # NOTE: not sure if RZ_A1H (only target with Cortex-A9) has tz
    # Also not sure if fpu is single or double precision
    "Cortex-A9": CortexA9(fpu=FloatingPoint.double_precision, tz=False),
    # Note these may not always be tz=True
    "Cortex-M23-NS": CortexM23(tz=True),
    "Cortex-M23": CortexM23(tz=True),
    "Cortex-M33-NS": CortexM33(tz=True),
    "Cortex-M33": CortexM33(tz=True),
    "Cortex-M33F-NS": CortexM33(fpu=FloatingPoint.single_precision, tz=True),
    "Cortex-M33F": CortexM33(fpu=FloatingPoint.single_precision, tz=True),
    "Cortex-M33FD-NS": CortexM33(fpu=FloatingPoint.double_precision, tz=True),
    "Cortex-M33FD": CortexM33(fpu=FloatingPoint.double_precision, tz=True),
}
