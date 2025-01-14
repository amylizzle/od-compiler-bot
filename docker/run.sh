#!/bin/sh
cp /app/code/* .
echo "---Preamble---"
echo Included compiler arguments: "$@"
echo "---Start Compiler---"
dotnet exec /opendream/compiler/DMCompiler.dll "$@" test.dme
echo "---End Compiler---"
echo "---Start Server---"
dotnet exec /opendream/server/Robust.Server.dll --config-file server_config.toml --cvar opendream.json_path=/app/test.json
echo "---End Server---"
