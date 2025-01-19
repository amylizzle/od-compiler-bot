import os
import tarfile
from pathlib import Path

import git
import wget
from git.repo import Repo
from od_compiler.util.compiler_logger import compile_logger

goonstation_git = "https://github.com/goonstation/goonstation.git"
rustg_git = "https://github.com/goonstation/rust-g.git"


def updateGoon(goon_path: Path, clean: int = False) -> bool:
    """
    Update the Goonstation repository if it exists. If it doesn't, clone a fresh copy.
    Returns True when a container rebuild is needed
    """
    if clean:
        from shutil import rmtree

        rmtree(goon_path)

    if Path.exists(goon_path):
        goon = Repo(goon_path)
        remote_latest_commit = git.cmd.Git().ls_remote(goonstation_git, "master")
        if remote_latest_commit.startswith(goon.head.commit.hexsha):
            compile_logger.info(f"The Goonstation repo is at: {goon.head.commit.hexsha} and does not need updating")
            return False
        # We reset HEAD to the upstream commit as a faster and more reliable way to stay up to date
        goon.remote().fetch(depth=1)
        goon.head.reset(commit="origin/master", working_tree=True)
    else:
        compile_logger.info("Repo not found. Cloning from GitHub.")
        goon = Repo.clone_from(
            url=goonstation_git,
            to_path=goon_path,
            multi_options=["--depth 1"],
        )

    # edit the __build.dm to run our test only
    with open(goon_path / "_std" / "__build.dm", "a") as builddm:
        builddm.writelines(["#define UNIT_TESTS\n", "#define UNIT_TEST_TYPES /datum/unit_test/od_compile_bot\n"])
    compile_logger.info(f"The Goonstation repo is updated to: {goon.head.commit.hexsha}")
    return False


def updateRustG(rg_path: Path, clean: int = False) -> bool:
    """
    Update the goonrustg repository if it exists. If it doesn't, clone a fresh copy.
    Returns True when a container rebuild is needed
    """
    if clean:
        from shutil import rmtree

        rmtree(rg_path)

    if Path.exists(rg_path):
        rg = Repo(rg_path)
        remote_latest_commit = git.cmd.Git().ls_remote(rustg_git, "master")
        if remote_latest_commit.startswith(rg.head.commit.hexsha):
            compile_logger.info(f"The rustg repo is at: {rg.head.commit.hexsha} and does not need updating")
            return False
        # We reset HEAD to the upstream commit as a faster and more reliable way to stay up to date
        rg.remote().fetch(depth=1)
        rg.head.reset(commit="origin/master", working_tree=True)
    else:
        compile_logger.info("Repo not found. Cloning from GitHub.")
        rg = Repo.clone_from(
            url=rustg_git,
            to_path=rg_path,
            multi_options=["--depth 1"],
        )

    # edit lib.rs to allow for 64 bit compile
    with open(rg_path / "src" / "lib.rs", "a") as librs:
        librs.seek(0, os.SEEK_END)
        librs.truncate(librs.tell() - 104)  # so hacky lol
    compile_logger.info(f"The goon-rustg repo is updated to: {rg.head.commit.hexsha}")
    return True


def updateOD(od_path: Path, clean: int = False) -> bool:
    """
    Update the OpenDream binaries.
    Returns True when a container rebuild is needed
    """

    compiler_path = od_path / "compiler.tar.gz"
    server_path = od_path / "server.tar.gz"
    tag_path = od_path / "tag"

    if clean:
        from shutil import rmtree

        rmtree(od_path)

    if not Path.exists(od_path):
        os.mkdir(od_path)
    remote_heads = git.cmd.Git().ls_remote("https://github.com/OpenDreamProject/OpenDream/", "master")
    tag_path.touch(exist_ok=True)
    with open(str(tag_path), "r+") as tag:
        if tag.readline() == remote_heads:
            compile_logger.info("OpenDream is already up to date.")
            return False
        else:
            tag.truncate(0)
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
    compile_logger.info(f"The OpenDream binaries are updated to: {remote_heads}")
    return True
