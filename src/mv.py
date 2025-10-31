from pathlib import Path
import shutil

def mv(args: list[str]):
    dst = Path(args.pop(-1))
    if len(args) == 1:
        shutil.move(Path(args[0]), dst)
        return None
    elif len(args) == 0:
        raise IndexError
    else:
        if dst.is_dir():
            for src in args:
                shutil.move(Path(src), dst)
            return None
        else:
            raise NotADirectoryError(f"{dst} is not a directory")