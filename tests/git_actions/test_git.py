import pytest
from od_compiler.util.git_actions import updateGoon
from od_compiler.util.git_actions import updateOD


def test_update_repo_clean(od_repo_path):
    updateOD(od_path=od_repo_path, clean=True)


@pytest.mark.depends(on=["test_update_repo_clean"])
def test_update_repo_existing(od_repo_path):
    updateOD(od_path=od_repo_path)


def test_update_goon_repo_clean(goon_repo_path):
    updateGoon(goon_path=goon_repo_path, clean=True)


@pytest.mark.depends(on=["test_update_goon_repo_clean"])
def test_update_goon_repo_existing(goon_repo_path):
    updateGoon(goon_path=goon_repo_path)
