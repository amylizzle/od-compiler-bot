import os
import tarfile
from pathlib import Path

import git
import wget
from git.repo import Repo
from od_compiler.util.compiler_logger import compile_logger


def updateGoon(goon_path: Path, clean: int = False) -> None:
    """
    Update the Goonstation repository if it exists. If it doesn't, clone a fresh copy.
    """
    if clean:
        from shutil import rmtree

        rmtree(goon_path)

    if Path.exists(goon_path):
        goon = Repo(goon_path)
        goon.remote().fetch()
        # We reset HEAD to the upstream commit as a faster and more reliable way to stay up to date
        goon.head.reset(commit="origin/master", working_tree=True)
    else:
        compile_logger.info("Repo not found. Cloning from GitHub.")
        goon = Repo.clone_from(
            url="https://github.com/goonstation/goonstation.git",
            to_path=goon_path,
            multi_options=["--depth 1"],
        )

    # edit the __build.dm to run our test only
    with open(goon_path / "_std" / "__build.dm", "a") as builddm:
        builddm.writelines(["#define UNIT_TESTS\n", "#define UNIT_TEST_TYPES /datum/unit_test/od_compile_bot\n"])
    compile_logger.info(f"The Goonstation repo is at: {goon.head.commit.hexsha}")


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
