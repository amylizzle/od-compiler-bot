FROM mcr.microsoft.com/dotnet/sdk:9.0-alpine AS builder


RUN adduser odcompile -H -D

WORKDIR /opendream

COPY --chown=odcompile ./OpenDream/ .

RUN ln -s /opendream/DMCompiler_linux-x64/DMCompiler /usr/bin/ && \
    ln -s /opendream/OpenDreamServer_linux-x64/Robust.Server /usr/bin

FROM builder

WORKDIR /app

COPY --chown=odcompile docker/run.sh .

USER odcompile

ENTRYPOINT [ "/bin/sh", "/app/run.sh" ]
