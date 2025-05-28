from main import main
import sys


def test_menu1():
    sys.stdin = open("test/inputs/test1")
    command = main(True)
    assert command == "ffmpeg -i infile outfile"
