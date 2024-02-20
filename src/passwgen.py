import click
from converters import default, config, folder
from encoder import encode
from os.path import exists, isdir


@click.command()
@click.option("--path", type=str, help="Path to the object", required=True)
@click.option("--length", type=int, help="Length of the password", default=20)
@click.option("--offset", type=int, help="Offset for generating passwords. Can be useful for generating several passwords from one source", default=0)
@click.option('--silent', is_flag=True)
def main(path: str, length: int, offset: int, silent: bool):
    """Generates password of given length based on the given file"""
    if length <= 0:
        return print("length param should be positive")
    if offset < 0:
        return print("offset param should be non-negative")
    if not exists(path):
        return print(f"{path} don't exist!")

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

if __name__ == '__main__':
    main()
