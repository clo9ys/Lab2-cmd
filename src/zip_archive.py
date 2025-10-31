import zipfile
from pathlib import Path

def make_zip(args: list[str]):
    if len(args) >= 2:
        zip_name = args.pop(-1)
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for arg in args:
                for file in Path(arg).rglob("*"):
                    zipf.write(file, arcname=Path(arg).name / file.relative_to(arg))

    else:
        raise IndexError("Not enough arguments")

def make_unzip(args: list[str]):
    for arg in args:
        with zipfile.ZipFile(arg, "r") as zipf:
            zipf.extractall(Path.cwd())
