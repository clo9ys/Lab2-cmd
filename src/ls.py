from pathlib import Path
from src.resolve import Resolve
import os
import datetime as dt
from stat import filemode

class Ls:
    def __init__(self, cwd=Path.cwd()):
        self.cwd = cwd

    def list_dir(self, args: list[str]):
        # Функция ls
        if len(args) == 0:
            print(*os.listdir(path=self.cwd), sep="  ")
            return None

        else:
            if args[0] == '-l':
                args.remove("-l")
                if len(args) == 0:
                    for pth in sorted(self.cwd.iterdir()):
                        Ls().l_flag(pth)
                    return None
                else:
                    for i in range(len(args)):
                        pth = Resolve().resolv(args[i])
                        if pth.is_file():
                            print(f"{args[i]}:")
                            Ls().l_flag(pth)
                        else:
                            print(f"{args[i]}:")
                            for p in sorted(pth.iterdir()):
                                Ls().l_flag(p)
                    return None
            else:
                Ls().arg_flag(args)
                return None

    @staticmethod
    def arg_flag(args: list[str]):
        if len(args) > 1:
            for i in range(len(args)):
                print(f"{args[i]}:\n", *os.listdir(path=args[i]), sep="  ")
            return 1
        else:
            print(*os.listdir(path=args[0]), sep="  ")
            return 1

    @staticmethod
    def l_flag(pth: Path):
        st = pth.stat()
        time_change = dt.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        name = pth.name
        size = st.st_size
        access = filemode(st.st_mode)
        print(f"{access:13} {time_change:10} {size:8}   {name}")