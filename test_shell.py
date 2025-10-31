import os
import pytest
from pathlib import Path
from main import Shell

@pytest.fixture
def temp_dir(tmp_path):
    # Создать временный рабочий каталог
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old_cwd)

@pytest.fixture
def shell():
    # Получить экземпляр консоли
    return Shell()

def test_cd(temp_dir, shell):
    new_dir = "new_dir"
    os.mkdir(new_dir)
    shell.run(f"cd {new_dir}")
    assert shell.cwd.name == new_dir

@pytest.mark.parametrize("home_dir", ["~", ""])
def test_cd_home(temp_dir, shell, home_dir):
    shell.run(f"cd {home_dir}")
    assert shell.cwd == Path.home()

def test_ls(shell, capsys, tmp_path):
    shell.run(f"ls {tmp_path}")
    out = capsys.readouterr().out
    # Директория не пуста, ls должен выводить содержимое
    list_dir = os.listdir(tmp_path)
    out_list = out.strip().split()
    assert out_list == list_dir

def test_cat(temp_dir, shell, capsys):
    file1 = "test.txt"
    data = "hello"
    with open(file1, "w") as f:
        f.write(data)
    shell.run(f"cat {file1}")
    out = capsys.readouterr().out
    assert data in out

def test_mv_and_rm(temp_dir, shell):
    src = "file1.txt"
    dst = "file2.txt"
    with open(src, "w") as f:
        f.write("something")
    shell.run(f"mv {src} {dst}")
    assert not os.path.exists(src)
    assert os.path.exists(dst)
    shell.run(f"rm {dst}")
    assert not os.path.exists(dst)

def test_cp(temp_dir, shell):
    src = "file1.txt"
    dst = "file2.txt"
    with open(src, "w") as f:
        f.write("something")
    shell.run(f"cp {src} {dst}")
    assert os.path.exists(dst)
    with open(dst) as f:
        assert f.read() == "something"

def test_rm_dir_recursive_accepted(temp_dir, shell, monkeypatch):
    os.mkdir("dir1")
    with open("dir1/file.txt", "w") as f:
        f.write("test")
    monkeypatch.setattr("builtins.input", lambda _: "y")
    shell.run("rm -r dir1")
    assert not os.path.exists("dir1")

def test_rm_dir_recursive_cancelled(temp_dir, shell, monkeypatch):
    os.mkdir("dir2")
    with open("dir2/file.txt", "w") as f:
        f.write("test")
    monkeypatch.setattr("builtins.input", lambda _: "n")
    shell.run("rm -r dir2")
    assert os.path.exists("dir2")

def test_unknown_command(temp_dir, shell, capsys):
    shell.run("top-it")
    out = capsys.readouterr().out
    assert "Unknown command" in out

@pytest.mark.parametrize("cmd", ["cat", "rm", "mv", "cp", "rm -r"])
def test_not_enough_args(temp_dir, shell, capsys, cmd):
    shell.run(cmd)
    out = capsys.readouterr().out
    assert 'Not enough arguments' in out
