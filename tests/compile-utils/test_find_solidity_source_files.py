import itertools
import os

from populus import Project
from populus.utils.filesystem import (
    is_same_path,
)


def test_gets_correct_files_default_dir(project_dir, write_project_file):
    project = Project(project_dir, create_config_file=True)
    compiler_backend = project.get_compiler_backend()
    file_names = tuple(itertools.chain.from_iterable(
        compiler_backend.get_project_source_paths(source_dir)
        for source_dir
        in project.contracts_source_dirs
    ))

    should_match = {
        'contracts/SolidityContract.sol',
        'contracts/AnotherFile.sol',
    }

    should_not_match = {
        'contracts/BackedUpContract.sol.bak',
        'contracts/Swapfile.sol.swp',
        'contracts/not-contract.txt',
    }

    for filename in should_match:
        write_project_file(filename)

    for filename in should_not_match:
        write_project_file(filename)

    for file_name in file_names:
        assert os.path.exists(file_name)
        assert any(is_same_path(file_name, path) for path in should_match)
        assert not any(is_same_path(file_name, path) for path in should_not_match)
