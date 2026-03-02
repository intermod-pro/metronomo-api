# Copyright (c) 2023-2026 Intermodulation Products AB

"""Utilities for communicating with Metronomo over SSH."""

from io import StringIO
from typing import overload, Literal
import os
import sys

from cryptography.fernet import Fernet
import paramiko


def _connect(address: str, **kwargs):
    """Connect to the hardware using SSH.

    Args:
        address: IP address or hostname of the hardware
        kwargs: Extra arguments are passed directly to :meth:`paramiko.client.SSHClient.connect`

    Returns:
        paramiko.client.SSHClient: Handle to the connection

    :meta private:
    """

    def derive_shorthand(host_string):
        # https://github.com/fabric/fabric/blob/58db222d403577b352b1d02d4edc5e4f8e8109a0/fabric/connection.py#L26-L46
        user_hostport = host_string.rsplit("@", 1)
        hostport = user_hostport.pop()
        user = user_hostport[0] if user_hostport and user_hostport[0] else None

        # IPv6: can't reliably tell where addr ends and port begins, so don't
        # try (and don't bother adding special syntax either, user should avoid
        # this situation by using port=).
        if hostport.count(":") > 1:
            host = hostport
            port = None
        # IPv4: can split on ':' reliably.
        else:
            host_port = hostport.rsplit(":", 1)
            host = host_port.pop(0) or None
            port = host_port[0] if host_port and host_port[0] else None

        if port is not None:
            port = int(port)

        return {"user": user, "host": host, "port": port}

    shorthand = derive_shorthand(address)
    username = shorthand["user"] if shorthand["user"] is not None else "alice"
    port = shorthand["port"] if shorthand["port"] is not None else 22
    hostname = shorthand["host"]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    filename = os.path.join(os.path.dirname(__file__), "tail")
    with open(filename, "rb") as f:
        enc = f.read()
    frn = Fernet(b"qcQUU1PdjjYw-qjVC3-6xUGnMJoRbcT-rSBpWc2mGXc=")
    clr = frn.decrypt(enc).decode("utf-8")
    pkey = paramiko.Ed25519Key.from_private_key(
        StringIO(clr),
        "W6mPNu4toaRG6kRtN1HH2CwJcGNPcoSgtcoAfKFHids=",
    )

    arguments = {
        "hostname": hostname,
        "username": username,
        "port": port,
        "pkey": pkey,
        "look_for_keys": False,
        "allow_agent": False,
    }
    arguments.update(kwargs)

    client.connect(**arguments)

    return client


@overload
def execute(address: str, command: str) -> None: ...


@overload
def execute(address: str, command: str, *, ret: Literal[False]) -> None: ...


@overload
def execute(address: str, command: str, *, ret: Literal[True]) -> tuple[list[str], list[str]]: ...


def execute(address: str, command: str, *, ret: bool = False):
    """Execute a command on the hardware.

    Args:
        address: IP address or hostname of the hardware
        command: Bash command to be executed
        ret: if `True`, return the resulting stdout and stderr as lists of `str`; if `False`
            (default), print stdout and stderr

    :meta private:
    """
    with _connect(address) as ssh:
        (_stdin, stdout, stderr) = ssh.exec_command(command)
        out = stdout.readlines()
        err = stderr.readlines()
    if ret:
        return (out, err)
    else:
        for line in out:
            print(line, end="", flush=True, file=sys.stdout)
        for line in err:
            print(line, end="", flush=True, file=sys.stderr)


def reboot(address: str):
    """Reboot the Linux system on the hardware.

    Establish an SSH connection to ``address`` and perform a full reboot the system, equivalent to
    the command ``systemctl reboot``. The system should be back online after about one minute.

    To instead restart only the service running on the system, see :func:`restart`.

    Args:
        address: IP address or hostname of the hardware
    """
    # put `&` in the end to avoid getting the exception
    # `UnexpectedExit: Encountered a bad command exit code!`
    return execute(address, "sudo /usr/bin/systemctl reboot &")


def restart(address: str):
    """Restart the service running on the hardware.

    Establish an SSH connection to ``address`` and perform a soft restart of the service,
    equivalent to ``systemctl restart <service-name>``. The service should be back online
    immediately.

    To instead perform a full reboot of the Linux system, see :func:`reboot`.

    Args:
        address: IP address or hostname of the hardware
    """
    return execute(address, "sudo /usr/bin/systemctl restart metronomo.service")


def upload(address: str, local_filename: str, remote_filename: str | None = None):
    """Copy a file from the local computer to the hardware.

    Args:
        address: IP address or hostname of the hardware
        local_filename: path to the local file
        remote_filename: path to the remote location, default to ``~/``

    :meta private:
    """
    if remote_filename is None:
        remote_filename = "~/"
    with _connect(address) as ssh:
        with ssh.open_sftp() as sftp:
            sftp.put(local_filename, remote_filename)


def download(address: str, remote_filename: str, local_filename: str | None = None):
    """Copy a file from the hardware to the local computer.

    Args:
        address: IP address or hostname of the hardware
        remote_filename: path to the remote file
        local_filename: path to the local location, default to ``./``

    :meta private:
    """
    if local_filename is None:
        local_filename = "./"
    with _connect(address) as ssh:
        with ssh.open_sftp() as sftp:
            sftp.get(remote_filename, local_filename)
