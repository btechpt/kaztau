from typing import Any, Dict, List, NamedTuple
from pathlib import Path
from kaztau.database import DatabaseHandler
from kaztau import DB_READ_ERROR, ID_ERROR


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

    def get_group(self, data_id: int) -> CurrentGroup:
        """Get data group using data id or index."""
        read = self._db_handler.read_groups()
        if read.error:
            return CurrentGroup({}, read.error)
        try:
            group = read.group_list[data_id - 1]
        except IndexError:
            return CurrentGroup({}, ID_ERROR)
        return CurrentGroup(group, read.error)

    def get_group_list(self) -> List[Dict[str, Any]]:
        """Return the current group list."""
        read = self._db_handler.read_groups()
        return read.group_list

    def set_verified(self, data_id: int, status: bool = True) -> CurrentGroup:
        """Set group as verify using data id or index."""
        read = self._db_handler.read_groups()
        if read.error:
            return CurrentGroup({}, read.error)
        try:
            group = read.group_list[data_id - 1]
        except IndexError:
            return CurrentGroup({}, ID_ERROR)
        group["verify"] = status
        write = self._db_handler.write_groups(read.group_list)
        return CurrentGroup(group, write.error)

    def remove(self, data_id: int) -> CurrentGroup:
        """Remove a group from the database using data id or index."""
        read = self._db_handler.read_groups()
        if read.error:
            return CurrentGroup({}, read.error)
        try:
            group = read.group_list.pop(data_id - 1)
        except IndexError:
            return CurrentGroup({}, ID_ERROR)
        write = self._db_handler.write_groups(read.group_list)
        return CurrentGroup(group, write.error)
