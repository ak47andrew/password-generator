import click
from src.config import config
from src.converters import default
from src.encoder import encode

@click.command()
@click.option("--path", type=str, help="Path to the object")
@click.option("--length", type=int, help="Length of the password")
def main(path: str, length: int):
    """Generates password of given length based on the given file"""
    ext = path.split(".")[-1].lower()
    command = config.get(ext, default)
    data = command(path)
    hash = encode(data, length,)
    print(f"Password is: {hash}")

if __name__ == '__main__':
    main()
