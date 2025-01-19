#!/bin/sh
cp /app/code/od_compile_bot.dm /opendream/goonstation/code/modules/unit_tests/od_compile_bot.dm
echo "---Preamble---"
echo Included compiler arguments: "$@"
echo "---Start Compiler---"
dotnet exec /opendream/compiler/DMCompiler.dll "$@" /opendream/goonstation/goonstation.dme
echo "---End Compiler---"
echo "---Start Server---"
dotnet exec /opendream/server/Robust.Server.dll --config-file server_config.toml --cvar opendream.json_path=/opendream/goonstation/goonstation.json
echo "---End Server---"
