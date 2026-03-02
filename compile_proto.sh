#!/usr/bin/env bash
set -euxo pipefail

PROTO="../metronomo-rs/proto"

uv run --resolution lowest-direct \
python \
    -m grpc_tools.protoc \
    --proto_path="${PROTO}" \
    --python_out=./metronomo/_rpc \
    --pyi_out=./metronomo/_rpc \
    --grpc_python_out=./metronomo/_rpc \
    "${PROTO}/metronomo.proto"

sed -i 's/^import metronomo_pb2/from . import metronomo_pb2/' ./metronomo/_rpc/metronomo_pb2_grpc.py
