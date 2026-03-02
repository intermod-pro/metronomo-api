# Copyright (c) 2023-2026 Intermodulation Products AB

"""Update the firmware on the Metronomo hardware.

This module is designed to be used from the command-line interface (CLI).

To get the help text, run the following command in a command-line terminal:

.. code-block:: bash

    python -m metronomo.updater --help

It will print something like this:

.. code-block:: text

    usage: python -m metronomo.updater [-h] [-f] -a ADDRESS [-p PORT] [--fw-ver FW_VER] filename

    positional arguments:
      filename              filename of the update bundle

    options:
      -h, --help            show this help message and exit
      -f, --force           force update
      -a, --address ADDRESS
                            Metronomo's IP address
      -p, --port PORT       Metronomo's SSH port number (default 22)
      --fw-ver FW_VER       firmware version to be installed

Typically, you would receive detailed instructions on how to update your Metronomo together with
the release announcement.
"""

import argparse
import os.path
import sys

from .ssh import execute, upload

_DEFAULT_SSH_PORT = 22


def compare_versions(ver1: str, ver2: str) -> int:
    ver1t = tuple(int(x) for x in ver1.split("."))
    ver2t = tuple(int(x) for x in ver2.split("."))
    if ver1t == ver2t:
        return 0
    elif ver1t > ver2t:
        return 1
    else:  # ver2t > ver1t
        return -1


def check_files(args) -> bool:
    if not os.path.isfile(args.filename):
        print(f'Update bundle "{args.filename}" not found')
        return False

    return True


def remote_version(address: str) -> str:
    (out, _err) = execute(address, "/usr/sbin/metronomo --version", ret=True)
    version = out[0].split()[1]
    return version


def ask_update() -> bool:
    while True:
        answer = input("Do you want to continue? [y/N]")
        if answer.lower() in ["y", "yes", "n", "no", ""]:
            break

    if answer in ["y", "yes"]:
        return True
    else:
        return False


def update(args):
    if not check_files(args):
        print("See --help for usage information")
        sys.exit(1)

    target = f"{args.address:s}:{args.port:d}"

    print(f"{args.fw_ver = }")

    installed_version = remote_version(target)
    print(f"Firmware version installed on Metronomo: {installed_version}")

    available_version = args.fw_ver if args.fw_ver is not None else "UNKNOWN"
    print(f"Firmware version available to upload:    {available_version}")

    do_it = False
    if args.fw_ver is not None:
        cmp = compare_versions(available_version, installed_version)
        print()
        if cmp == 0:
            print(f"Metronomo is up to date: {installed_version}")
            if not args.force:
                print('(use flag "--force" to force reinstall)')
        elif cmp > 0:
            print(f"Metronomo can be updated: {installed_version} --> {available_version}")
        else:  # cmp < 0
            print(f"Metronomo can be DOWNGRADED: {installed_version} --> {available_version}")
            if not args.force:
                print('(use flag "--force" to force downgrade)')

        print()
        if cmp <= 0 and not args.force:
            print("Nothing to do.. Bye!")
        else:
            if cmp == 0:
                print("Metronomo's firmware will be reinstalled.")
            elif cmp > 0:
                print("Metronomo's firmware will be updated.")
            else:  # cmp < 0
                print("Metronomo's firmware will be DOWNGRADED.")

            do_it = ask_update()
    else:
        do_it = ask_update()

    if do_it:
        basename = os.path.basename(args.filename)
        remote_filename = f"/home/alice/update/{basename}"
        upload(target, args.filename, remote_filename)
        execute(target, f"sudo /usr/sbin/mtrupd {remote_filename}")
        print("All good... Bye!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", help="force update", action="store_true")
    parser.add_argument("-a", "--address", help="Metronomo's IP address", required=True)
    parser.add_argument(
        "-p",
        "--port",
        help=f"Metronomo's SSH port number (default {_DEFAULT_SSH_PORT})",
        default=_DEFAULT_SSH_PORT,
        type=int,
    )
    parser.add_argument(
        "--fw-ver",
        help="firmware version to be installed",
    )
    parser.add_argument("filename", help="filename of the update bundle")
    args = parser.parse_args()

    update(args)
