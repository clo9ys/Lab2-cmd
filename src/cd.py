from pathlib import Path
import os
from src.resolve import Resolve

class Cd:
    def __init__(self, cwd=Path):
        self.cwd = cwd

    def change_dir(self, args: list[str]):
        # Функция cd
        if not args or args[0] == "~":
            new_cwd = Path.home()  # Домашняя директория

        else:
            new_cwd = Resolve().resolv(pth=args[0])  # Названная директория

        os.chdir(new_cwd)  # Меняем директорию
        self.cwd = new_cwd
        return self.cwd  # Передаем новую директорию в main