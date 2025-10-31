from pathlib import Path
import shutil

def cp(args: list[str]):
    dst = Path(args.pop(-1))
    if args[0] != "-r":
        if len(args) == 1:
            shutil.copy2(Path(args[0]), dst)
        else:
            if dst.is_dir():
                for src in args:
                    shutil.copy2(Path(src), dst)
            else:
                raise NotADirectoryError(f"{dst} is not a directory")
    else:
        args.remove("-r")
        r_flag(args, dst)


def r_flag(args: list[str], dst):
    if dst.is_dir():
        for src in args:
            src1 = Path(src)
            if src1.is_dir():
                shutil.copytree(src1, dst / src1.name, dirs_exist_ok=True)
            else:
                raise NotADirectoryError(f"{src1} is not a directory")
    else:
        raise NotADirectoryError(f"{dst} is not a directory")