from pathlib import Path
import datetime as dt, shlex
from src.ls import Ls
from src.cat import cat
from src.cd import Cd
from src.mv import mv
from src.rm import rm
from src.cp import cp
from src.logger import make_logger
from src.help import _help

class Shell:
    def __init__(self):
        self.cwd = Path.cwd() # Текущая рабочая директория
        self.logger = make_logger()

    def parser(self):
        while True:
            try:
                line = input(f"{self.cwd}> ") # Выводим пользователю текущую рабочую директорию, затем считываем команду

            except (EOFError, KeyboardInterrupt):
                print()
                break

            self.run(line)

    @staticmethod
    def add_history(line: str):
        with open(".history", "a", encoding="utf-8") as f:
            time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{time}] {line}\n")

    def run(self, line: str):
        Shell().add_history(line)
        self.logger.info(f" - {line}")
        cmd, *args = shlex.split(line.strip())
        try:
            match cmd:
                case "ls":
                    Ls(self.cwd).list_dir(args)

                case "cd":
                    self.cwd = Cd(self.cwd).change_dir(args)

                case "cat":
                    cat(args)

                case "mv":
                    mv(args)

                case "rm":
                    rm(args)

                case "cp":
                    cp(args)

                case "--help":
                    _help(args)

                case "exit":
                    raise SystemExit(0) # функция завершения работы программы при вводе "exit"

                case _:
                    print(f"Unknown command: {cmd}")
                    self.logger.error(f" - unknown command")

        except (FileNotFoundError, FileExistsError):
            print(f"No such file or directory")
            self.logger.error(f" - wrong argument")
        except NotADirectoryError as err:
            print(err)
            self.logger.error(" - wrong argument")
        except PermissionError as err:
            print(err)
            self.logger.error(f" - user don't have enough permissions")
        except IndexError:
            print("Not enough arguments")
            self.logger.error(" - not enough arguments")

if __name__ == "__main__":
    Shell().parser()
