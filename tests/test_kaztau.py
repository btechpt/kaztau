import json
import pytest
from typer.testing import CliRunner
from kaztau import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    kaztau,
)

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    groups = [{"group_id": "gr-tele", "owner": "parman", "verify": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(groups, db, indent=4)
    return db_file


test_data1 = {
    "group_id": "gr-1",
    "name": "group ops",
    "group": {
        "group_id": "gr-1",
        "name": "group ops",
        "verify": False,
    },
}
test_data2 = {
    "group_id": "gr-2",
    "name": "group dev",
    "group": {
        "group_id": "gr-2",
        "name": "group dev",
        "verify": False,
    },
}


@pytest.mark.parametrize(
    "group_id, owner, expected",
    [
        pytest.param(
            test_data1["group_id"],
            test_data1["name"],
            (test_data1["group"], SUCCESS),
        ),
        pytest.param(
            test_data2["group_id"],
            test_data2["name"],
            (test_data2["group"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, group_id, owner, expected):
    grouper = kaztau.Grouper(mock_json_file)
    assert grouper.add(group_id, owner) == expected
    read = grouper._db_handler.read_groups()
    assert len(read.group_list) == 2
