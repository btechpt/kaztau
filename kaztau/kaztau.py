from typing import Any, Dict, List, NamedTuple
from pathlib import Path
from kaztau.database import DatabaseHandler
from kaztau import DB_READ_ERROR


class CurrentGroup(NamedTuple):
    group: Dict[str, Any]
    error: int


class Grouper:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, group_id: str, name: str = "") -> CurrentGroup:
        """Add a new group to the database."""
        group = {
            "group_id": group_id,
            "name": name,
            "verify": False,
        }
        read = self._db_handler.read_groups()
        if read.error == DB_READ_ERROR:
            return CurrentGroup(group, read.error)
        read.group_list.append(group)
        write = self._db_handler.write_groups(read.group_list)
        return CurrentGroup(group, write.error)

    def get_group_list(self) -> List[Dict[str, Any]]:
        """Return the current group list."""
        read = self._db_handler.read_groups()
        return read.group_list
