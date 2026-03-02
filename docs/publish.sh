#!/usr/bin/bash
set -euxo pipefail

scp -r _build/html/* intermod.pro@ssh.intermod.pro:/www/manuals/metronomo/
