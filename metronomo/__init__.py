# Copyright (c) 2023-2026 Intermodulation Products AB

"""Entry point for controlling the Metronomo hardware."""

import socket
import sys

import grpc
from grpc._channel import _InactiveRpcError

from .utils import eprint_error
from ._rpc import metronomo_pb2 as mty
from ._rpc import metronomo_pb2_grpc as mrpc

__version__ = "1.1.0"
VERSION = __version__

_DEFAULT_PORT = 7879
_FW_NAME = "metronomo"
_FW_VER = "0.2.1"


class Metronomo:
    def __init__(
        self,
        address: str,
        port: int = _DEFAULT_PORT,
        *,
        err_on_ver_mismatch: bool = True,
    ):
        r"""A handle to the Metronomo hardware.

        Warning:
            This class is designed to be instantiated with Python's
            :ref:`with statement <python:with>`, see Examples section.

        Args:
            address: IP address or hostname of the hardware
            port: port number of the server running on the hardware. If :obj:`None`, use factory
                default ``7879``
            err_on_ver_mismatch: if ``True`` (default), raise an exception if the firmware version
                on the hardware does not match the version expected by this API. Set to ``False`` to
                instead just print a warning message.

        Raises:
            RuntimeError: if the version of the API is incompatible with the version of the
                firmware running on Metronomo

        Examples:
            Connect to Metronomo, select external reference clock, wait for a lock, and output a
            synchronization pulse:

            >>> from metronomo import Metronomo
            >>> with Metronomo("172.23.40.1") as mtr:
            >>>     mtr.set_ref_external(10e6)
            >>>     mtr.wait_for_lock()
            >>>     mtr.sync_out()
        """
        # grpc doesn't seem to resolve .local domains, so do the resolution ourselves
        # limit output to IPv4 TCP
        (_family, _type, _proto, _canonname, _sockaddr) = socket.getaddrinfo(
            host=address,
            port=port,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )[0]
        target = f"{_sockaddr[0]:s}:{_sockaddr[1]:d}"

        self._channel = grpc.insecure_channel(target)
        self._stub = mrpc.MetronomoStub(self._channel)

        idn = self._idn()
        if idn.name != _FW_NAME:
            raise RuntimeError(f"expected to connect to {_FW_NAME}, got {idn.name} instead")
        if idn.version != _FW_VER:
            msg = f"expected firmware version {_FW_VER}, got {idn.version} instead"
            if err_on_ver_mismatch:
                raise RuntimeError(msg)
            else:
                msg += ". Things might not work as expected!"
                eprint_error("WARN", msg, warn=True, inline=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close the connection to Metronomo.

        This method is called automatically upon exit from a :ref:`with block <python:with>`.
        """
        self._channel.close()

    def _try(self, rpc, arg):
        try:
            return rpc(arg)
        except _InactiveRpcError as err:
            if err.code() is grpc.StatusCode.INTERNAL:
                err_str = (
                    f"\x1b[1;31m{' SERVER ERROR ':-^80}\x1b[0m"
                    f"\n{err.details()}\n"
                    f"\x1b[1;31m{'':-^80}\x1b[0m"
                )
                raise RuntimeError(f"got errors from Metronomo, check the log below\n{err_str:s}")
            else:
                raise

    def _idn(self) -> mty.IdnRet:
        resp: mty.IdnRet = self._try(self._stub.Idn, mty.IdnArg())
        return resp

    def get_firmware_version(self) -> str:
        """Version of the firmware running on Metronomo."""
        reply = self._idn()
        return reply.version

    def _echo(self, value: int) -> int:
        resp: mty.EchoRet = self._try(self._stub.Echo, mty.EchoArg(value=value))
        return resp.value

    def sleep(self, secs: float):
        """Tell Metronomo to sleep for ``secs`` seconds.

        Like :func:`time.sleep`, except the sleep is done on Metronomo rather than on the local
        computer.

        Args:
            secs: duration of sleep in seconds
        """
        _resp: mty.SleepRet = self._try(self._stub.Sleep, mty.SleepArg(seconds=secs))

    def _clk_reset(self):
        """Perform a software reset of the LMK04832 chip, i.e. assert the RESET bit.

        The clock configuration is be clearead, no outputs are active. Use :meth:`reset` for
        "resetting" to a working default configuration.

        See also:
            reset
        """
        _resp: mty.ClkResetRet = self._try(self._stub.ClkReset, mty.ClkResetArg())

    def _clk_program(self):
        """Program the LMK04832 with the default configuration.

        Will perform a software reset first.
        """
        _resp: mty.ClkProgramRet = self._try(self._stub.ClkProgram, mty.ClkProgramArg())

    def reset(self):
        """Reset the clocks to the default configuration."""
        self._clk_program()

    def _clk_ref(self, external: bool, frequency: float) -> float:
        resp: mty.ClkRefRet = self._try(
            self._stub.ClkRef,
            mty.ClkRefArg(
                external=external,
                frequency=frequency,
            ),
        )
        return resp.frequency

    def set_ref_internal(self) -> float:
        """Program Metronomo to use the internal reference clock.

        Returns:
            the internal reference clock frequency in hertz

        Examples:
            >>> mtr.set_ref_internal()
            10000000.0

        """
        return self._clk_ref(False, 0.0)

    def set_ref_external(self, ref_freq: float = 10e6) -> float:
        """Program Metronomo to use an external reference clock.

        Args:
            ref_freq: frequency in Hz of the external reference, default 10 MHz

        Returns:
            the reference clock frequency that was configured, in hertz

        Notes:
            Not all reference clock frequencies are supported. If the user requests an unsupported
            clock frequency, it will be rounded to the nearest supported frequency. The frequency
            that is actually programmed is returned.

        Examples:
            100 MHz is a supported frequency

            >>> mtr.set_ref_external(100e6)
            100000000.0

            17 MHz is not supported, rounded to 15 MHz

            >>> mtr.set_ref_external(17e6)
            15000000.0
        """
        return self._clk_ref(True, ref_freq)

    def _set_sysref_mode(self, mode: mty.SysrefMode):
        _resp: mty.SetSysrefModeRet = self._try(
            self._stub.SetSysrefMode, mty.SetSysrefModeArg(mode=mode)
        )

    def _set_sysref_continuous(self):
        self._set_sysref_mode(mty.SYSREF_MODE_CONTINUOUS)

    def _set_sysref_pulser(self):
        self._set_sysref_mode(mty.SYSREF_MODE_PULSER)

    def set_out_clk_freq(self, out_freq: float):
        """Set frequency of all output clocks.

        Args:
            out_freq: output clock frequency in hertz

        Returns:
            the output clock frequency that was configured, in hertz

        Notes:
            Not all output clock frequencies are supported. If the user requests an unsupported
            clock frequency, it will be rounded to the nearest supported frequency. The frequency
            that is actually programmed is returned.

        Examples:
            1 GHz is a supported frequency

            >>> mtr.set_out_clk_freq(1e9)
            1000000000.0

            700 MHz is not supported, rounded to 750 MHz

            >>> mtr.set_out_clk_freq(700e6)
            750000000.0
        """
        resp: mty.ClkOutFreqRet = self._try(
            self._stub.ClkOutFreq,
            mty.ClkOutFreqArg(frequency=out_freq),
        )
        return resp.frequency

    def sync_out(self):
        """Output a synchronization pulse (sysref pulse) on all Sync ports."""
        _resp: mty.SyncOutRet = self._try(self._stub.SyncOut, mty.SyncOutArg())

    def is_locked(self) -> bool:
        """Check whether Metronomo is locked to a reference clock."""
        resp: mty.IsLockedRet = self._try(self._stub.IsLocked, mty.IsLockedArg())
        return resp.locked

    def wait_for_lock(self) -> int:
        """Wait for Metronomo to lock to the reference clock.

        The current thread on the local computer will block until the PLL locks.
        """
        resp: mty.WaitForLockRet = self._try(self._stub.WaitForLock, mty.WaitForLockArg())
        return resp.milliseconds

    def _test_fail(self, value: int) -> None:
        """Test failures on the GRPC server.

        Arg:
            failure code

        Notes:
            - 0: (success)
            - 1: cancelled
            - 2: unknown
            - 3: invalid_argument
            - 4: deadline_exceeded
            - 5: not_found
            - 6: already_exists
            - 7: permission_denied
            - 8: resource_exhausted
            - 9: failed_precondition
            - 10: aborted
            - 11: out_of_range
            - 12: unimplemented
            - 13: internal <-- what we return in case of error
            - 14: unavailable
            - 15: data_loss
            - 16: unauthenticated
            - 17..: (trigger a panic!)

        See also:
            https://github.com/grpc/grpc/blob/master/doc/statuscodes.md#status-codes-and-their-use-in-grpc

        :meta private:
        """
        _resp: mty.TestFailRet = self._try(self._stub.TestFail, mty.TestFailArg(value=value))
