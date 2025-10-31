from warnings import catch_warnings

from src.mv import mv
from pathlib import Path
from src.logger import make_logger

def rm(args: list[str]):
    trash = Path(".trash")
    trash.mkdir(exist_ok=True)
    if args[0] != "-r":
        for src in args:
            src1 = Path(src)
            if src1.is_file():
                mv([src1, ".trash"])
            else:
                raise FileNotFoundError(f"{src} is not a file, if you want remove a directory use -r")
    else:
        args.remove("-r")
        r_flag(args[0])

def r_flag(src):
    src1 = Path(src)
    if not is_root(src1):
        if src1.is_dir():
            while True:
                answ = input(f"Delete directory {src}? [y/n]: ").lower()
                if answ == "y":
                    mv([src1, ".trash"])
                    make_logger().info("Directory was delete")
                    break
                elif answ == "n":
                    print("Delete was canceled")
                    make_logger().info("Delete was canceled")
                    break
                else:
                    print("Wrong answer: print 'y' or 'n' (yes or no).")
        else:
            raise NotADirectoryError(f"{src} is not a directory, if you want remove a file dont use -r")
    else:
        raise PermissionError(f"You cant remove this directory: {src1}")

def is_root(path: Path) -> bool:
    path = path.resolve()
    if (str(path) == "/" or (path.parent == path and path.drive) or
            (path == Path.cwd().parent.resolve()) or (path == Path.cwd().resolve())):
        return True
    return False