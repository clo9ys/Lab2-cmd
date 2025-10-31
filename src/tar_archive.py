import tarfile
from pathlib import Path

def make_tar(args: list[str]):
    if len(args) >= 2:
        tar_name = args.pop(-1)
        with tarfile.open(tar_name, "w:gz") as tarf:
            for arg in args:
                for file in Path(arg).rglob("*"):
                    tarf.add(file, arcname=Path(arg).name / file.relative_to(arg))

    else:
        raise IndexError("Not enough arguments")

def make_untar(args: list[str]):
    for arg in args:
        with tarfile.open(arg, "r:gz") as tarf:
            tarf.extractall(Path.cwd())