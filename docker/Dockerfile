FROM mcr.microsoft.com/dotnet/runtime:9.0-alpine AS builder


RUN adduser odcompile -H -D
RUN apk add libsodium-dev
RUN apk add cargo

WORKDIR /opendream

COPY ./rustg ./rustg
RUN cd ./rustg && cargo build --release

COPY --chown=odcompile ./OpenDream/ .
COPY --chown=odcompile ./goonstation ./goonstation/

RUN ln -s /opendream/DMCompiler_linux-x64/ /opendream/compiler
RUN ln -s /opendream/OpenDreamServer_linux-x64/ /opendream/server

RUN cp ./rustg/target/release/librust_g.so /opendream/goonstation/librust_g.so

FROM builder

WORKDIR /app

COPY docker/run.sh .

USER odcompile

ENTRYPOINT [ "/bin/sh", "/app/run.sh", "--suppress-unimplemented"]
