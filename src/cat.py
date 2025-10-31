from src.resolve import Resolve

def cat(args: list[str]):
    if not args:
        raise IndexError("Not enough arguments")

    for arg in args:
        file1 = Resolve().resolv(pth=arg)

        if not file1.exists() or not file1.is_file():
            raise FileNotFoundError("No such file")

        with open(file1, "r", encoding="UTF-8") as f:
            print(f"{arg}:\n\n", f.read())
    return 0

