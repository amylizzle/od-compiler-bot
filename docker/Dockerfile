FROM mcr.microsoft.com/dotnet/sdk:9.0-alpine AS builder


WORKDIR /opendream

COPY ./OpenDream/ .

ARG BULD_CONFIG=Release

RUN ln -s /opendream/DMCompiler_linux-x64/DMCompiler /usr/bin/ && \
    ln -s /opendream/OpenDreamServer_linux-x64/Robust.Server /usr/bin

FROM builder

WORKDIR /app

COPY docker/run.sh .

ENTRYPOINT [ "/bin/sh", "/app/run.sh" ]
