from os.path import exists, isdir
from os import remove

import click
import requests as r

from converters import config, default, folder
from encoder import encode


@click.command()
@click.option("--path", type=str, help="Path to the object")
@click.option("--uri", type=str, help="Uri to the object")
@click.option("--length", type=int, help="Length of the password", default=20)
@click.option("--offset", type=int, help="Offset for generating passwords. Can be useful for generating several passwords from one source", default=0)
@click.option('--silent', is_flag=True)
def main(path: str, uri: str, length: int, offset: int, silent: bool):
    """Generates password of given length based on the given file"""
    if (not path and not uri) or (path and uri):
        return print("You should specify either --url or --path")
    if length <= 0:
        return print("length param should be positive")
    if offset < 0:
        return print("offset param should be non-negative")
    if path is not None and not exists(path):
        return print(f"{path} don't exist!")

    try:
        if uri is not None:
            if not (uri.startswith("http://") or uri.startswith("https://")):
                uri = "http://" + uri
            path = uri.split("/")[-1]
            if not silent:
                print(f"Downloading file from {uri} to {path}...")
            try:
                with open(path, "wb") as f:
                    f.write(r.get(uri, timeout=60).content)
            except r.exceptions.ReadTimeout as e:
                return print(f"Timed out! {e}.\nTry again in a few minutes")
            except r.exceptions.ConnectionError as e:
                return print(f"An error has occurred!\n{e}")
            if not silent:
                print("Done!")

        if isdir(path):
            if not silent:
                print("You specified folder. This can start a very long process")
            data = folder(path, silent)
            if not data:
                return print("No data found in folder! Make sure it contains at least one not empty file")
        else:
            ext = path.split(".")[-1].lower()
            command = config.get(ext, default)
            data = command(path, silent)
        hash = encode(data, length, offset)
        print(hash if silent else f"Password is: {hash}")
    finally:
        if uri is not None:
            remove(path)

if __name__ == '__main__':
    main()
