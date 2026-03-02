from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SysrefMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYSREF_MODE_PULSER: _ClassVar[SysrefMode]
    SYSREF_MODE_CONTINUOUS: _ClassVar[SysrefMode]
SYSREF_MODE_PULSER: SysrefMode
SYSREF_MODE_CONTINUOUS: SysrefMode

class IdnArg(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IdnRet(_message.Message):
    __slots__ = ("name", "version", "serial_number", "rpi_model", "rpi_soc", "rpi_serial", "pcb_serial")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    RPI_MODEL_FIELD_NUMBER: _ClassVar[int]
    RPI_SOC_FIELD_NUMBER: _ClassVar[int]
    RPI_SERIAL_FIELD_NUMBER: _ClassVar[int]
    PCB_SERIAL_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    serial_number: str
    rpi_model: str
    rpi_soc: str
    rpi_serial: str
    pcb_serial: str
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., serial_number: _Optional[str] = ..., rpi_model: _Optional[str] = ..., rpi_soc: _Optional[str] = ..., rpi_serial: _Optional[str] = ..., pcb_serial: _Optional[str] = ...) -> None: ...

class EchoArg(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class EchoRet(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class SleepArg(_message.Message):
    __slots__ = ("seconds",)
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    seconds: float
    def __init__(self, seconds: _Optional[float] = ...) -> None: ...

class SleepRet(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClkResetArg(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClkResetRet(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClkProgramArg(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClkProgramRet(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClkRefArg(_message.Message):
    __slots__ = ("external", "frequency")
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    external: bool
    frequency: float
    def __init__(self, external: bool = ..., frequency: _Optional[float] = ...) -> None: ...

class ClkRefRet(_message.Message):
    __slots__ = ("frequency",)
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    frequency: float
    def __init__(self, frequency: _Optional[float] = ...) -> None: ...

class ClkOutFreqArg(_message.Message):
    __slots__ = ("frequency",)
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    frequency: float
    def __init__(self, frequency: _Optional[float] = ...) -> None: ...

class ClkOutFreqRet(_message.Message):
    __slots__ = ("frequency",)
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    frequency: float
    def __init__(self, frequency: _Optional[float] = ...) -> None: ...

class WaitForLockArg(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WaitForLockRet(_message.Message):
    __slots__ = ("milliseconds",)
    MILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    milliseconds: int
    def __init__(self, milliseconds: _Optional[int] = ...) -> None: ...

class IsLockedArg(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IsLockedRet(_message.Message):
    __slots__ = ("locked",)
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    locked: bool
    def __init__(self, locked: bool = ...) -> None: ...

class SetSysrefModeArg(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: SysrefMode
    def __init__(self, mode: _Optional[_Union[SysrefMode, str]] = ...) -> None: ...

class SetSysrefModeRet(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SyncOutArg(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SyncOutRet(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestFailArg(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class TestFailRet(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
