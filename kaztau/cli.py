import typer

from typing import List, Optional
from pathlib import Path
from kaztau import (
    ERRORS, __app_name__, __version__, config, database, kaztau
)
from kaztau.notifications import Notification
from kaztau.utils import get_all_path_file_from_folder, checking_dir, move_file
from kaztau.exceptions import KaztauError
from kaztau import whatsapp


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
        try:
            notif = Notification()
            typer.secho("Sending .... !", fg=typer.colors.BLUE)
            notif.send(group['group_id'], message)
        except KaztauError as e:
            typer.secho(e, fg=typer.colors.RED)
            raise typer.Exit(1)
        typer.secho(
            f"""# success send message to "{group['name']}" """,
            fg=typer.colors.GREEN,
        )


@app.command(name="send_image")
def send_image(
    data_id: int = typer.Argument(...),
    path_file: str = typer.Option(None),
    move_folder: Optional[str] = typer.Option(None)
) -> None:
    """To send image."""
    grouper = get_grouper()
    group, error = grouper.get_group(data_id)
    if error:
        typer.secho(
            f'Data id # "{data_id}" failed open or not found: "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        if move_folder and not checking_dir(move_folder):
            typer.secho(f"Directory move not found: {move_folder}", fg=typer.colors.RED)
            raise typer.Exit(1)

        try:
            notif = Notification()
            typer.secho("Sending .... !", fg=typer.colors.BLUE)
            notif.send_image(group['group_id'], path_file)
        except KaztauError as e:
            typer.secho(e, fg=typer.colors.RED)
            raise typer.Exit(1)

        typer.secho(f"""Success send file to "{group['name']}" """, fg=typer.colors.GREEN)

        if move_folder:
            move_file(move_folder, path_file)
            typer.secho(f"""Success move image to "{move_folder}" """, fg=typer.colors.GREEN)


@app.command(name="send_multi_image")
def send_multi_image(
    data_id: int = typer.Argument(...),
    path_file: Optional[List[str]] = typer.Option(None),
    path_folder: Optional[str] = typer.Option(None),
    move_folder: Optional[str] = typer.Option(None)
) -> None:
    """To send multi image."""
    grouper = get_grouper()
    group, error = grouper.get_group(data_id)
    if error:
        typer.secho(
            f'Data id # "{data_id}" failed open or not found: "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        if path_folder:
            if not checking_dir(path_folder):
                typer.secho(f"Directory image not found: {path_folder}", fg=typer.colors.RED)
                raise typer.Exit(1)
            images = get_all_path_file_from_folder(path_folder)
        else:
            for path in path_file:
                if not checking_dir(path):
                    typer.secho(f"file not found: {path}", fg=typer.colors.RED)
                    raise typer.Exit(1)
            images = path_file

        if not images:
            typer.secho(f"No images in directory: {path_folder}", fg=typer.colors.RED)
            raise typer.Exit(1)

        if move_folder and not checking_dir(move_folder):
            typer.secho(f"Directory move not found: {move_folder}", fg=typer.colors.RED)
            raise typer.Exit(1)

        try:
            notif = Notification()
            typer.secho("Sending .... !", fg=typer.colors.BLUE)
            notif.send_multi_image(group['group_id'], images)
        except KaztauError as e:
            typer.secho(e, fg=typer.colors.RED)
            raise typer.Exit(1)

        typer.secho(f"""Success send file to "{group['name']}" """, fg=typer.colors.GREEN)

        if move_folder:
            for image in images:
                move_file(move_folder, image)
            typer.secho(f"""Success move images to "{move_folder}" """, fg=typer.colors.GREEN)


@app.command(name="send_wa_message")
def send_wa_message(
    number: str = typer.Argument(...),
    message: str = typer.Option(2, "--message", "-m", min=1)
) -> None:
    """To send wa message."""
    try:
        typer.secho("Sending .... !", fg=typer.colors.BLUE)
        whatsapp.wa_send_message(identifier=number, message=message)
    except KaztauError as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(
        f"""# success send message to "{number}" """,
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
