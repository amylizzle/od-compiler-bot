FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS builder

WORKDIR /opendream

COPY ./OpenDream/ .

ARG BULD_CONFIG=Release

RUN ln -s /opendream/bin/DMCompiler_linux-x64/DMCompiler /usr/bin/ && \
    ln -s /opendream/bin/OpenDreamServer_linux-x64/Robust.Server /usr/bin

FROM builder

WORKDIR /app

COPY docker/run.sh .

RUN adduser odcompile -H -D && \
    chown -R odcompile: /app && \
	chown -R odcompile: /opendream/bin

USER odcompile

ENTRYPOINT [ "/bin/sh", "/app/run.sh" ]
