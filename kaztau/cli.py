import typer

from typing import List, Optional
from pathlib import Path
from kaztau import (
    ERRORS, __app_name__, __version__, config, database, kaztau
)
from kaztau.notifications import Notification
app = typer.Typer()


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="kaztau database location?",
    ),
) -> None:
    """Initialize the kaztau database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The kaztau database is {db_path}", fg=typer.colors.GREEN)


def get_grouper() -> kaztau.Grouper:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "kaztau init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return kaztau.Grouper(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "kaztau init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def add(
    group_id: str = typer.Argument(...),
    owner: str = typer.Option(2, "--name", "-n", min=1, max=3),
) -> None:
    """Add a new group chat."""
    grouper = get_grouper()
    group, error = grouper.add(group_id, owner)
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""group: "{group['group_id']} - {group['name']}" was added """,
            fg=typer.colors.GREEN,
        )


@app.command(name="list")
def list_all() -> None:
    """List of chat groups."""
    grouper = get_grouper()
    group_list = grouper.get_group_list()
    if len(group_list) == 0:
        typer.secho(
            "There are no groups chat.", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nGroup list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Group ID  ",
        "| Verify  ",
        "| Name  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, group in enumerate(group_list, 1):
        group_id, name, verify = group.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({group_id}){(len(columns[1]) - len(str(group_id)) - 4) * ' '}"
            f"| {verify}{(len(columns[2]) - len(str(verify)) - 2) * ' '}"
            f"| {name}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


@app.command(name="verified")
def set_verified(data_id: int = typer.Argument(...)) -> None:
    """Set verified."""
    grouper = get_grouper()
    group, error = grouper.set_verified(data_id)
    if error:
        typer.secho(
            f'Data id # "{data_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""# {data_id} "{group['name']}" is verified!""",
            fg=typer.colors.GREEN,
        )


@app.command(name="unverified")
def set_unverified(data_id: int = typer.Argument(...)) -> None:
    """Set to unverified."""
    grouper = get_grouper()
    group, error = grouper.set_verified(data_id, status=False)
    if error:
        typer.secho(
            f'Data id # "{data_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""# {data_id} "{group['name']}" is unverified!""",
            fg=typer.colors.GREEN,
        )


@app.command()
def remove(
    data_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove a group using its data id."""
    grouper = get_grouper()

    def _remove():
        group, error = grouper.remove(data_id)
        if error:
            typer.secho(
                f'Removing group # {group["group_id"]} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""group # {group['group_id']}: {group['name']} was removed""",
                fg=typer.colors.GREEN,
            )

    if force:
        _remove()
    else:
        group_list = grouper.get_group_list()
        try:
            group = group_list[data_id - 1]
        except IndexError:
            typer.secho("Invalid data id", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete group # {group['group_id']}: {group['name']}?"
        )
        if delete:
            _remove()
        else:
            typer.echo("Operation canceled")


@app.command(name="send_message")
def send_message(
        data_id: int = typer.Argument(...),
        message: str = typer.Option(2, "--message", "-m", min=1)
) -> None:
    """To send message."""
    grouper = get_grouper()
    group, error = grouper.get_group(data_id)
    if error:
        typer.secho(
            f'Data id # "{data_id}" failed open or not found: "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        notif = Notification()
        notif.send(group['group_id'], message)
        typer.secho(
            f"""# success send message to "{group['name']}" """,
            fg=typer.colors.GREEN,
        )


@app.command(name="send_file")
def send_file(
        data_id: int = typer.Argument(...),
        path_file: str = typer.Option(2, "--pathfile", "-pf", min=1)
) -> None:
    """To send file."""
    grouper = get_grouper()
    group, error = grouper.get_group(data_id)
    if error:
        typer.secho(
            f'Data id # "{data_id}" failed open or not found: "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        notif = Notification()
        notif.send_file(group['group_id'], path_file)
        typer.secho(
            f"""# success send file to "{group['name']}" """,
            fg=typer.colors.GREEN,
        )


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
