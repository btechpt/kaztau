import typer

from typing import List, Optional
from kaztau import (
    __app_name__, __version__
)
from kaztau.utils import get_all_path_file_from_folder, checking_dir, move_file
from kaztau.exceptions import KaztauError
from kaztau import whatsapp
from kaztau import telegram


app = typer.Typer()


@app.command(name="send_wa_message")
def send_wa_message(
    identifier: str = typer.Argument(...),
    message: str = typer.Argument(...),
    to_group: bool = typer.Option(False, "--togroup")
) -> None:
    """To send wa message."""
    try:
        typer.secho("Sending .... !", fg=typer.colors.BLUE)
        whatsapp.wa_send_message(identifier=identifier, message=message, to_group=to_group)
    except KaztauError as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(
        f"""# success send message to "{identifier}" """,
        fg=typer.colors.GREEN,
    )


@app.command(name="send_wa_image")
def send_wa_image(
    identifier: str = typer.Argument(...),
    message: str = typer.Argument(...),
    img_path: str = typer.Argument(...),
    to_group: bool = typer.Option(False, "--togroup"),
    move_folder: str = typer.Option("")
) -> None:
    """To send wa image."""
    if move_folder and not checking_dir(move_folder):
        typer.secho(f"Directory move not found: {move_folder}", fg=typer.colors.RED)
        raise typer.Exit(1)

    try:
        typer.secho("Sending .... !", fg=typer.colors.BLUE)
        whatsapp.wa_send_file(
            identifier=identifier,
            path_file=img_path,
            message=message,
            to_group=to_group
        )
    except KaztauError as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"""# success send message to "{identifier}" """, fg=typer.colors.GREEN)

    if move_folder:
        move_file(move_folder, img_path)
        typer.secho(f"""Success move image to "{move_folder}" """, fg=typer.colors.GREEN)


@app.command(name="send_wa_multi_image")
def send_wa_multi_image(
    identifier: str = typer.Argument(...),
    message: str = typer.Argument(...),
    path_file: Optional[List[str]] = typer.Option(None),
    path_folder: Optional[str] = typer.Option(None),
    to_group: bool = typer.Option(False, "--togroup"),
    move_folder: str = typer.Option("")
) -> None:
    """To send wa image."""
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

    for image in images:
        try:
            typer.secho("Sending .... !", fg=typer.colors.BLUE)
            whatsapp.wa_send_file(
                identifier=identifier,
                path_file=image,
                message=message,
                to_group=to_group
            )
            typer.secho(f"""... success send image "{image}" """, fg=typer.colors.BLUE)
        except KaztauError as e:
            typer.secho(e, fg=typer.colors.RED)
            raise typer.Exit(1)

    typer.secho(f"""# success send all images to "{identifier}" """, fg=typer.colors.GREEN)

    if move_folder:
        for image in images:
            move_file(move_folder, image)
        typer.secho(f"""Success move images to "{move_folder}" """, fg=typer.colors.GREEN)


@app.command(name="send_telegram_message")
def send_telegram_message(
    identifier: str = typer.Argument(...),
    message: str = typer.Argument(...),
) -> None:
    """To send telegram message."""
    try:
        typer.secho("Sending .... !", fg=typer.colors.BLUE)
        telegram.bot_send_message(identifier, message)
    except KaztauError as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(
        f"""# success send message to "{identifier}" """,
        fg=typer.colors.GREEN,
    )


@app.command(name="send_telegram_image")
def send_telegram_image(
    identifier: str = typer.Argument(...),
    img_path: str = typer.Argument(...),
    move_folder: str = typer.Option("")
) -> None:
    """To send telegram image."""
    if move_folder and not checking_dir(move_folder):
        typer.secho(f"Directory move not found: {move_folder}", fg=typer.colors.RED)
        raise typer.Exit(1)

    try:
        typer.secho("Sending .... !", fg=typer.colors.BLUE)
        telegram.bot_send_file(identifier, img_path)
    except KaztauError as e:
        typer.secho(e, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"""# success send message to "{identifier}" """, fg=typer.colors.GREEN)

    if move_folder:
        move_file(move_folder, img_path)
        typer.secho(f"""Success move image to "{move_folder}" """, fg=typer.colors.GREEN)


@app.command(name="send_telegram_multi_image")
def send_telegram_multi_image(
    identifier: str = typer.Argument(...),
    path_file: Optional[List[str]] = typer.Option(None),
    path_folder: Optional[str] = typer.Option(None),
    move_folder: str = typer.Option("")
) -> None:
    """To send telegram multi images."""
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

    for image in images:
        try:
            typer.secho("Sending .... !", fg=typer.colors.BLUE)
            telegram.bot_send_file(identifier, image)
            typer.secho(f"""... success send image "{image}" """, fg=typer.colors.BLUE)
        except KaztauError as e:
            typer.secho(e, fg=typer.colors.RED)
            raise typer.Exit(1)

    typer.secho(f"""# success send all images to "{identifier}" """, fg=typer.colors.GREEN)

    if move_folder:
        for image in images:
            move_file(move_folder, image)
        typer.secho(f"""Success move images to "{move_folder}" """, fg=typer.colors.GREEN)


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
