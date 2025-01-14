import os
import tarfile
from pathlib import Path

import git
import wget
from od_compiler.util.compiler_logger import compile_logger


def updateOD(od_path: Path, clean: int = False) -> None:
    """
    Update the OpenDream repository if it exists. If it doesn't, clone a fresh copy.
    """

    compiler_path = od_path / "compiler.tar.gz"
    server_path = od_path / "server.tar.gz"
    tag_path = od_path / "tag"

    if clean:
        from shutil import rmtree

        rmtree(od_path)

    if not Path.exists(od_path):
        os.mkdir(od_path)
    remote_heads = git.cmd.Git().ls_remote("https://github.com/OpenDreamProject/OpenDream/", heads=True)
    tag_path.touch(exist_ok=True)
    with open(str(tag_path), "r+") as tag:
        if tag.readline() == remote_heads:
            compile_logger.info("OpenDream is already up to date.")
            return
        else:
            tag.seek(0)
            tag.write(remote_heads)

    if compiler_path.exists():
        os.remove(compiler_path)
    if server_path.exists():
        os.remove(server_path)
    wget.download(
        "https://github.com/OpenDreamProject/OpenDream/releases/download/latest/DMCompiler_linux-x64.tar.gz",
        str(compiler_path),
    )
    wget.download(
        "https://github.com/OpenDreamProject/OpenDream/releases/download/latest/OpenDreamServer_linux-x64.tar.gz",
        str(server_path),
    )

    with tarfile.open(str(compiler_path), "r:gz") as tar:
        tar.extractall(path=od_path)
    with tarfile.open(str(server_path), "r:gz") as tar:
        tar.extractall(path=od_path)
    compile_logger.info(f"The OpenDream repo is at: {remote_heads}")
