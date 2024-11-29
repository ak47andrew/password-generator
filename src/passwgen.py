from os.path import exists, isdir
from os import remove
import sys

import click
import requests as r

from converters import config, default, folder
from encoder import encode


def handle_uri(uri: str, silent: bool):
    if not (uri.startswith("http://") or uri.startswith("https://")):
        uri = "http://" + uri
    path = uri.split("/")[-1]
    if not silent:
        print(f"Downloading file from {uri} to {path}...")
    try:
        with open(path, "wb") as f:
            f.write(r.get(uri, timeout=None).content)
    except r.exceptions.ReadTimeout as e:
        return print(f"Timed out! {e}.\nTry again in a few minutes")
    except r.exceptions.ConnectionError as e:
        return print(f"An error has occurred!\n{e}")
    if not silent:
        print("Done!")
    return path


def handle_folder(path: str, silent: bool):
    if not silent:
        print("You specified folder. This can start a very long process")
    data = folder(path, silent)
    if not data:
        print("No data found in folder! Make sure it contains at least one not empty file")
        sys.exit(1)
    return data


def handle_file(path: str, silent: bool):
    ext = path.split(".")[-1].lower()
    command = config.get(ext, default)
    return command(path, silent)


def main(path: str, uri: str, length: int, silent: bool) -> str:
    if (not path and not uri) or (path and uri):
        print("You should specify either --url or --path")
        sys.exit(1)
    if length <= 0:
        print("length param should be positive")
        sys.exit(1)
    if path is not None and not exists(path):
        print(f"{path} don't exist!")
        sys.exit(1)

    try:
        if uri is not None:
            path = handle_uri(uri, silent)  # type: ignore 
            if path is None:
                return ""

        if isdir(path):
            data = handle_folder(path, silent)
        else:
            data = handle_file(path, silent)
        passw = encode(data, length)
        return passw
    finally:
        if uri is not None:
            remove(path)


@click.command()
@click.option("--path", type=str, help="Path to the object")
@click.option("--uri", type=str, help="Uri to the object")
@click.option("--length", type=int, help="Length of the password", default=20)
@click.option('--silent', is_flag=True)
def cli_wrapper(path: str, uri: str, length: int, silent: bool):
    """Generates password of given length based on the given file"""
    passw = main(path, uri, length, silent)
    print(passw if silent else f"Password is: {passw}")

if __name__ == '__main__':
    cli_wrapper()
